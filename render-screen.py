from app.parts.WeatherNowIcon import WeatherNowIcon
from pickle import TRUE
from PIL import Image
from app.parts.clockdate import ClockDate
from app.parts.nameday import NamedayFinderLanguage
from app.epaper import Epaper
import os

from app.parts.weather_hourly_graph import WeatherHourlyGraph

# Because of rende debuging without unit, the resolution of the resulting image must be set here 
width, height = 1872, 1404
debug = False

language = NamedayFinderLanguage.SK

# Main image, tjat will be rendered on e-paper
# this file should generate 4bit grayscale image that can be used directly into wireshare eing display
# image size for waveshare 7.8 HD epaper is 1872×1404 
img = Image.new("L", (width, height), color=255)

clock = ClockDate(scale=1.0, language=language)
clock.draw_clock(img, position=(10, -70))



# Part thats render actual weather info
icon_renderer = WeatherNowIcon(
    json_path="assets/weather-actual.json", # path to json
    icons_dir="external/weather-icons/icons/svg", # path to weather icons
    scale=1.3 # scale of the icon
)

hourly = WeatherHourlyGraph(
    weather_json_path="assets/weather-actual.json",
    position=(25, 880), 
    size=(1750, 500) 
)
hourly.draw(img)


# Draw the info
icon_renderer.render_icon(img, position=(1480, 100))  # veľkosť sa zistí automaticky

# path to save the last image for partial redraw
image_path = "assets/image.png"

# for debuging without unit, jet render and save the image
if debug:
    img.save(image_path)
    exit()

ep = Epaper()


if os.path.exists(image_path):
    ep.display.prev_frame = Image.open(image_path).convert("L")

# draw with partial redraw
ep.drawImage(img)
img.save(image_path)
