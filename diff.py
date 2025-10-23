from PIL import Image, ImageChops, ImageDraw
import os
import numpy as np

# Cesty k vstupným a výstupnému obrázku
img1_path = "export/image1.png"
img2_path = "export/image2.png"
diff_path = "export/diff.png"

# Načítanie obrázkov
img1 = Image.open(img1_path).convert("RGB")
img2 = Image.open(img2_path).convert("RGB")

# Vytvorenie diff obrázka
diff_img = ImageChops.difference(img1, img2)

# Detekcia zmenených pixelov
try:
    from scipy.ndimage import label, find_objects
    diff_np = np.array(diff_img)
    gray = diff_np[:, :, 0]  # použijeme len červený kanál (pre čiernobiely obrázok)
    mask = gray > 0  # maska zmenených pixelov
    labels, num = label(mask)
    boxes = find_objects(labels)
    # Vykreslenie obdlžnikov do diff obrázka
    draw = ImageDraw.Draw(diff_img)
    for box in boxes:
        if box is not None:
            y0, y1 = box[0].start, box[0].stop
            x0, x1 = box[1].start, box[1].stop
            draw.rectangle([x0, y0, x1, y1], outline="red", width=2)
except ImportError:
    print("scipy.ndimage nie je dostupné, obdlžniky nebudú vykreslené.")

# Uloženie diff obrázka
os.makedirs(os.path.dirname(diff_path), exist_ok=True)
diff_img.save(diff_path)
print(f"Diff image saved as {diff_path}")
