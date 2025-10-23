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
          self.display = AutoEPDDisplay(vcom=-1.56, spi_hz=24000000) 
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

        self.display.draw_full(DisplayModes.GC16)

     def drawImageDiff(self, imageActual: Image, imageNew: Image):
          # first get difference image
          diff_img = ImageChops.difference(imageActual, imageNew)
          diff_np = np.array(diff_img)
          # Ak je diff_np 2D (L mode), použijeme priamo, inak použijeme len červený kanál
          gray = diff_np if diff_np.ndim == 2 else diff_np[:, :, 0]
          mask = gray > 0  # maska zmenených pixelov
          labels, num = label(mask)
          boxes = find_objects(labels)

          for box in boxes:
              if box is not None:
                  y0, y1 = box[0].start, box[0].stop
                  x0, x1 = box[1].start, box[1].stop
                  # Vyrežeme zmenený výsek z nového obrázka
                  crop = imageNew.crop((x0, y0, x1, y1))
                  # Vložíme výsek na správnu pozíciu na frame_buf
                  self.display.frame_buf.paste(crop, (x0, y0))

          # Po všetkých zmenách vykreslíme len zmenené oblasti
          self.display.draw_full(DisplayModes.GC16)
