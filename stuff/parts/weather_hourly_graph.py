import json
from PIL import Image, ImageDraw, ImageFont
import datetime

class WeatherHourlyGraph:

    def draw_horizontal_grid_lines(self, draw, x0, y0, margin, plot_width, plot_height, plot_min, plot_max, temp_to_y):
        # Draw horizontal grid lines every 10°C starting from 0, with labels
        try:
            font = ImageFont.truetype("assets/fonts/raela-grotesque/RaelaGrotesqueRegular-e9476.ttf", 20)
        except:
            font = ImageFont.load_default()
        t = 0
        # Upwards
        while t <= plot_max:
            y = temp_to_y(t)
            if y0 + margin <= y <= y0 + margin + plot_height:
                draw.line([(x0 + margin, y), (x0 + margin + plot_width, y)], fill=64, width=1)
                draw.text((x0 - 5, y - 10), f"{int(t)}°C", font=font, fill=64)
            t += 10
        # Downwards
        t = -10
        while t >= plot_min:
            y = temp_to_y(t)
            if y0 + margin <= y <= y0 + margin + plot_height:
                draw.line([(x0 + margin, y), (x0 + margin + plot_width, y)], fill=64, width=1)
                draw.text((x0 - 5, y - 10), f"{int(t)}°C", font=font, fill=64)
            t -= 10

    def draw_current_time_marker(self, draw, dt_times, idx_to_x, y0, margin, plot_height):
        # Find the index of the closest hour to now
        now = datetime.datetime.now()
        if not dt_times:
            return
        # Find the closest index
        idx = min(range(len(dt_times)), key=lambda i: abs((dt_times[i] - now).total_seconds()))
        x = idx_to_x(idx)
        y_top = y0 + margin
        y_bottom = y0 + margin + plot_height
        draw.line([(x, y_top), (x, y_bottom)], fill=0, width=5)

    def draw_axes_and_labels(self, draw, x0, y0, margin, plot_width, plot_height, plot_min, plot_max, temp_to_y, idx_to_x, dt_times, n):
        # Font for labels
        try:
            font = ImageFont.truetype("assets/fonts/raela-grotesque/RaelaGrotesqueRegular-e9476.ttf", 24)
        except:
            font = ImageFont.load_default()
        # Draw axes
        draw.line([(x0 + margin, y0 + margin), (x0 + margin, y0 + margin + plot_height)], fill=0, width=2)
        draw.line([(x0 + margin, y0 + margin + plot_height), (x0 + margin + plot_width, y0 + margin + plot_height)], fill=0, width=2)
        # Draw y-axis ticks (min, 0, max) without labels
        for t in [plot_min, 0, plot_max]:
            if t < plot_min or t > plot_max:
                continue
            y = temp_to_y(t)
            draw.line([(x0 + margin - 5, y), (x0 + margin, y)], fill=0, width=2)
        # Draw x-axis hour ticks (both large and small) and labels
        label_step = max(1, n // 8)
        tick_height = 10
        tick_height_long = 22
        axis_y = y0 + margin + plot_height
        axis_center = axis_y
        for i in range(n):
            x = idx_to_x(i)
            dt = dt_times[i]
            if dt.hour == 0:
                # Longer, thicker tick for 00:00
                h = tick_height_long
                w = 3
                # Draw thin vertical grid line for day boundary
                y_top = y0 + margin
                y_bottom = y0 + margin + plot_height
                draw.line([(x, y_top), (x, y_bottom)], fill=200, width=1)
            else:
                h = tick_height
                w = 1
            # Center the tick on the axis (extends up and down)
            y1 = axis_center - h // 2
            y2 = axis_center + h // 2
            draw.line([(x, y1), (x, y2)], fill=0, width=w)
        # Draw labels less frequently for clarity
        for i in range(0, n, label_step):
            dt = dt_times[i]
            label = f"{dt.hour:02d}\n{dt.day}."
            x = idx_to_x(i)
            y = axis_center + tick_height_long // 2 + 2
            draw.text((x-10, y), label, font=font, fill=0, align="center")

    def draw_temperature_line(self, draw, temps, idx_to_x, temp_to_y, n):
        points = [(idx_to_x(i), temp_to_y(temps[i])) for i in range(n)]
        if len(points) > 1:
            draw.line(points, fill=0, width=3)
        for x, y in points:
            draw.ellipse([x-3, y-3, x+3, y+3], fill=0)

    def __init__(self, weather_json_path, position=(0, 0), size=(800, 300)):
        self.weather_json_path = weather_json_path
        self.position = position  # (x, y) where to draw the graph
        self.size = size  # (width, height) of the graph
        self.hourly = self._load_hourly()

    def _load_hourly(self):
        with open(self.weather_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("hourly", {})

    def draw(self, img):
        draw = ImageDraw.Draw(img)
        x0, y0 = self.position
        width, height = self.size
        margin = 50
        # Get data
        times = self.hourly.get("time", [])
        temps = self.hourly.get("temperature_2m", [])
        if not times or not temps:
            return  # nothing to plot

        # If times is a single value, but temps is a list, generate times for each hour
        if len(times) == 1 and len(temps) > 1:
            # Assume each temp is one hour after the first
            times = [times[0] + 3600 * i for i in range(len(temps))]
        elif len(times) != len(temps):
            # If lengths mismatch, try to match as much as possible
            n = min(len(times), len(temps))
            times = times[:n]
            temps = temps[:n]

        # Convert times to datetime
        dt_times = [datetime.datetime.utcfromtimestamp(t) for t in times]
        n = min(len(dt_times), len(temps))
        temps = temps[:n]
        dt_times = dt_times[:n]

        # Find min/max temp for scaling
        min_temp = min(temps)
        max_temp = max(temps)

        # Add some padding
        pad = 2
        plot_min = min(min_temp, 0) - pad
        plot_max = max(max_temp, 0) + pad

        # Calculate scaling
        plot_height = height - 2 * margin
        plot_width = width - 2 * margin
        def temp_to_y(temp):
            # Higher temp = lower y (top of image)
            return y0 + margin + plot_height * (plot_max - temp) / (plot_max - plot_min)

        def idx_to_x(idx):
            return x0 + margin + plot_width * idx / (n - 1 if n > 1 else 1)

        # (moved: all hour tick logic is now in draw_axes_and_labels)

        self.draw_horizontal_grid_lines(draw, x0, y0, margin, plot_width, plot_height, plot_min, plot_max, temp_to_y)
        self.draw_axes_and_labels(draw, x0, y0, margin, plot_width, plot_height, plot_min, plot_max, temp_to_y, idx_to_x, dt_times, n)

        # Draw current time marker
        self.draw_current_time_marker(draw, dt_times, idx_to_x, y0, margin, plot_height)
        # Draw temperature line and points LAST (above all other elements)
        self.draw_temperature_line(draw, temps, idx_to_x, temp_to_y, n)

