# this file should generate 4bit grayscale image that can be used directly into wireshare eing display
# image size for waveshare 7.8 HD epaper is 1872×1404 

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import locale
from parts.functions import *
from datetime import datetime
from parts.namesday.nameday import NamedayFinder, NamedayFinderLanguage



# the resolution of the resulting image
width, height = 1872, 1404
# here put your language code. note that the language code is not the same as the country code 
# not all languages are supported, check enum NamedayFinderLanguage
language = NamedayFinderLanguage.SK 

place = "Žilina, Slovensko" # here put your place name
days_array = ["Po", "Ut", "St", "Št", "Pi", "So", "Ne"] # needed for calendar value, so ho locale need to be installed

namesdayFinder = NamedayFinder("image-generator/parts/namesday/nameday.json")

# create a new pure white image with the given resolution
img = Image.new("L", (width, height), color=255)
imgDraw = ImageDraw.Draw(img)

# first show the clock

smallFont = ImageFont.truetype("image-generator/fonts/raela-grotesque/RaelaGrotesqueLight-0v1ER.ttf", 30)
mediumFont = ImageFont.truetype("image-generator/fonts/raela-grotesque/RaelaGrotesqueLight-0v1ER.ttf", 45)
timefont = ImageFont.truetype("image-generator/fonts/raela-grotesque/RaelaGrotesqueRegular-e9476.ttf", 100)

imgDraw.text( [20,20], place, font=smallFont, fill=0)
imgDraw.text( [20,40], datetime.now().strftime("%H:%M"), font=timefont, fill=0)
imgDraw.text( [20,150], get_date(days_array), font=mediumFont, fill=0)
imgDraw.text( [20,200], f"meniny: {namesdayFinder.find_nameday(datetime.now().day, datetime.now().month, language)}", font=smallFont, fill=0)



# store the image
img.save("export/image.png")
