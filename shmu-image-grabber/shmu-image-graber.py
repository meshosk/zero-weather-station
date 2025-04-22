import requests
from PIL import Image


# URL na stiahnutie
url = "https://www.shmu.sk/data/dataradary/data.cmax/cmax.kruh.20250422.1825.0.png"

# Názov súboru, pod ktorým sa uloží
output_file = "assets/tmp/cmax.kruh.20250422.1825.0.png"
converted_file = "assets/tmp/cmax.kruh.20250422.1825.0_converted.png"
conversion_map_file = "assets/storm-gradient.png"  # Prevodový obrázok

# Stiahnutie súboru
response = requests.get(url)
if response.status_code == 200:
    with open(output_file, "wb") as file:
        file.write(response.content)
    print(f"Súbor bol úspešne stiahnutý ako {output_file}")

    # Načítanie prevodového obrázka
    conversion_map = Image.open(conversion_map_file)
    original_colors = [conversion_map.getpixel((x, 0)) for x in range(conversion_map.width)]
    target_colors = [conversion_map.getpixel((x, 1)) for x in range(conversion_map.width)]

    # Načítanie pôvodného obrázka
    img = Image.open(output_file).convert("RGBA")  # Načítame s alfa kanálom
    converted_img = Image.new("RGBA", img.size)

    # Konverzia farieb podľa prevodového obrázka
    for x in range(img.width):
        for y in range(img.height):
            r, g, b, a = img.getpixel((x, y))  # Získame aj hodnotu alfa kanála
            if a == 0:
                # Ak je pixel transparentný, ponecháme ho nezmenený
                converted_img.putpixel((x, y), (r, g, b, a))
            elif (r, g, b) in original_colors:
                # Nájdeme index pôvodnej farby a použijeme zodpovedajúcu cieľovú farbu
                index = original_colors.index((r, g, b))
                converted_img.putpixel((x, y), (*target_colors[index], a))
            else:
                # Ak farba nie je v prevodovom obrázku, necháme ju nezmenenú
                converted_img.putpixel((x, y), (r, g, b, a))

    # Uloženie skonvertovaného obrázka
    converted_img.save(converted_file)
    print(f"Obrázok bol skonvertovaný a uložený ako {converted_file}")
else:
    print(f"Chyba pri sťahovaní súboru: {response.status_code}")