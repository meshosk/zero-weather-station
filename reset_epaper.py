from app.epaper import Epaper
from PIL import Image
import os
import time

time.sleep(30) #make delay from classic redraw

epd = Epaper()
epd.reset_screen()

# Zobraz obrazok z export/image.png, ak existuje
image_path = "assets/image.png"
if os.path.exists(image_path):
	try:
		img = Image.open(image_path)
		epd.drawImage(img, fullRedraw=False)
		print(f"Image {image_path} displayed with full redraw.")
	except Exception as e:
		print(f"Failed to display image: {e}")

print("Display was reset with anti-ghosting sequence.")
