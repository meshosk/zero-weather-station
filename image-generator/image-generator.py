# this file should generate 4bit grayscale image that can be used directly into wireshare eing display
# image size for waveshare 7.8 HD epaper is 1872×1404 

from PIL import Image
import numpy as np


# 1. Vytvorenie nového 8-bit grayscale obrázka (napr. gradient)
width, height = 1872, 1404

gradient = np.tile(np.arange(width, dtype=np.uint8), (height, 1))
img = Image.fromarray(gradient, mode='L')  # 8-bit grayscale

img.save("obrazok.bmp")
