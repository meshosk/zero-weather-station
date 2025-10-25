# this file should generate 4bit grayscale image that can be used directly into wireshare eing display
# image size for waveshare 7.8 HD epaper is 1872×1404 

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import locale
from stuff.functions import *
from datetime import datetime
from stuff.namesday.nameday import NamedayFinder, NamedayFinderLanguage

from stuff.epaper import Epaper
import os




# the resolution of the resulting image
width, height = 1872, 1404
# here put your language code. note that the language code is not the same as the country code 
# not all languages are supported, check enum NamedayFinderLanguage
language = NamedayFinderLanguage.SK 

place = "Žilina, Slovensko" # here put your place name
days_array = ["Po", "Ut", "St", "Št", "Pi", "So", "Ne"] # needed for calendar value, so ho locale need to be installed

namesdayFinder = NamedayFinder("stuff/namesday/nameday.json")

# create a new pure white image with the given resolution
img = Image.new("L", (width, height), color=255)
imgDraw = ImageDraw.Draw(img)

# first show the clock 

smallFont = ImageFont.truetype("assets/fonts/raela-grotesque/RaelaGrotesqueLight-0v1ER.ttf", 100)
mediumFont = ImageFont.truetype("assets/fonts/raela-grotesque/RaelaGrotesqueLight-0v1ER.ttf", 250)
timefont = ImageFont.truetype("assets/fonts/raela-grotesque/RaelaGrotesqueRegular-e9476.ttf", 550)

# imgDraw.text( [20,20], place, font=smallFont, fill=0)
imgDraw.text( [20,20], datetime.now().strftime("%H:%M"), font=timefont, fill=0)
imgDraw.text( [20, 700], get_date(days_array), font=mediumFont, fill="#696868")
imgDraw.text( [20,970], f"meniny: {namesdayFinder.find_nameday(datetime.now().day, datetime.now().month, language)}", font=smallFont, fill="#949492")


image_path = "export/image.png"

img.save(image_path);
exit()

ep = Epaper()


if os.path.exists(image_path):
    # this loads previous frame into new instance. Cron runs this script every 1 minute
    # if the image exists
    ep.display.prev_frame = Image.open(image_path).convert("L")

# draw with partial redraw
ep.drawImage(img)
# store new frame as previous
img.save(image_path)
