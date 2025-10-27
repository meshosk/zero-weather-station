from IT8951.interface import EPD
from IT8951.display import AutoEPDDisplay, VirtualEPDDisplay
from IT8951.constants import DisplayModes


import numpy as np
from PIL import Image, ImageDraw, ImageChops
from scipy.ndimage import label, find_objects

class Epaper():
     
     def __init__(self):
          # init display, change const params or attrinbs to fit your display
          # size of display is auto detected
          self.display = AutoEPDDisplay(vcom=-1.80, spi_hz=24000000) 
         # self.display = VirtualEPDDisplay()

     def fillScreen(self, color=0xFF):
          # def cleat whole display white
          self.display.frame_buf.paste(0xFF, box=(0, 0, self.display.width, self.display.height))

     def drawImage(self, image: Image):

        # size of display
        dims = (self.display.width, self.display.height)

        # restricitng image size. Rendered image on display will not exceed its dimensions
        image.thumbnail(dims)
        # this sets up possition of image on screenn
        paste_coords = [dims[i] - image.size[i] for i in (0,1)]  # align image with bottom of display
        self.display.frame_buf.paste(image, paste_coords)

        self.display.draw_partial(DisplayModes.GLD16)

     def reset_screen(self):
          """
          Resetuje e-ink displej sekvenciou plných prekreslení (biela, čierna, biela),
          aby sa odstránilo ghostovanie a pretekanie.
          """
          # Plná biela
          self.display.frame_buf.paste(0xFF, box=(0, 0, self.display.width, self.display.height))
          self.display.draw_full(DisplayModes.GC16)
          # Plná čierna
          self.display.frame_buf.paste(0x00, box=(0, 0, self.display.width, self.display.height))
          self.display.draw_full(DisplayModes.GC16)
          # Opäť biela
          self.display.frame_buf.paste(0xFF, box=(0, 0, self.display.width, self.display.height))
          self.display.draw_full(DisplayModes.GC16)