from IT8951.interface import EPD
from IT8951.display import AutoEPDDisplay
from IT8951 import constants

import numpy as np
from PIL import Image, ImageDraw

class Epaper():
     
     def __init__(self, json_file_path: str):
          # init display, change const params or attrinbs to fit your display
          # size of display is auto detected
          self.display = AutoEPDDisplay(vcom=-1.56, spi_hz=24000000) 

     def fillScreen(self, color=0xFF):
          # def cleat whole display white
          self.display.frame_buf.paste(0xFF, box=(0, 0, self.display.width, self.display.height))

     def drawImage(self, image: Image):

        # size of display
        dims = (self.display.width, self.display.height)

        # restricitng image size. Rendered image on display will not exceed its dimensions
        image.thumbnail(dims)
        # this sets up possition of image on screenn
        paste_coords = [dims[i] - img.size[i] for i in (0,1)]  # align image with bottom of display
        self.display.frame_buf.paste(image, paste_coords)

        self.display.draw_full(constants.DisplayModes.GC16)