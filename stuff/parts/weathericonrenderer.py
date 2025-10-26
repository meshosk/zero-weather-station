import json
from PIL import Image
import os


class WeatherIconRenderer:

    def __init__(self, json_path="export/weather-actual.json", icons_dir="assets/weather-icons/svg", scale=1.0):
        self.json_path = json_path
        self.icons_dir = icons_dir
        self.scale = scale


    def render_temperature_text(self, img, position, icon_size, scale, font_size=95):
    
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                weather = json.load(f)
            temp = weather["current"].get("temperature_2m", None)
            apparent = weather["current"].get("apparent_temperature", None)
            precipitation = weather["current"].get("precipitation", None)
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("assets/fonts/raela-grotesque/RaelaGrotesqueRegular-e9476.ttf", font_size)
            except:
                font = ImageFont.load_default()
            text_x = position[0]
            text_y = position[1] + int(icon_size[1] * scale * 1.05)
            if temp is not None and apparent is not None:
                text = f"{round(temp)}°C/{round(apparent)}°C"
                draw.text((text_x, text_y), text, font=font, fill=0)
                text_y += font_size + 5
            
            if precipitation is not None:
                
                if precipitation <= 1.0:
                    percent = int(round(precipitation * 100))
                else:
                    percent = int(round(precipitation))
                pr_text = f"{percent}%"
                draw.text((text_x, text_y), pr_text, font=font, fill="#696868")
        except Exception as e:
            print(f"Chyba pri vykresľovaní teploty: {e}")



    def get_weather_code(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        code = data["current"]["weather_code"]
        return str(int(round(code)))

    def get_icon_path(self, code):
     
        return os.path.join(self.icons_dir, f"{code}.svg")

    def render_icon(self, img, position=(0, 0), size=None, show_temperature=True):
        code = self.get_weather_code()
        icon_path = self.get_icon_path(code)
        
        if size is None:
            try:
                import xml.etree.ElementTree as ET
                tree = ET.parse(icon_path)
                root = tree.getroot()
                width = root.attrib.get("width")
                height = root.attrib.get("height")
               
                if width and width.endswith("px"): width = width[:-2]
                if height and height.endswith("px"): height = height[:-2]
                width = int(float(width)) if width else 256
                height = int(float(height)) if height else 256
                size = (width, height)
            except Exception as e:
          
                size = (256, 256)
        scaled_size = (int(size[0] * self.scale), int(size[1] * self.scale))
        try:
            import cairosvg
            import io
            png_bytes = cairosvg.svg2png(url=icon_path, output_width=scaled_size[0], output_height=scaled_size[1])
            from PIL import Image as PILImage
            icon_img = PILImage.open(io.BytesIO(png_bytes)).convert("LA")  # grayscale + alpha
           
            icon_gray, icon_alpha = icon_img.split()
          
            img.paste(icon_gray, position, mask=icon_alpha)
            if show_temperature:
                self.render_temperature_text(img, position, size, self.scale)
            print(f"Weather icon {icon_path} rendered and pasted at {position} with scale {self.scale}")
        except ImportError:
            print("Chýba knižnica cairosvg. Nainštalujte ju cez pip install cairosvg.")
        except Exception as e:
            print(f"Chyba pri renderovaní SVG: {e}")

        
