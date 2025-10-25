from PIL import ImageDraw, ImageFont
from datetime import datetime

from stuff.namesday.nameday import NamedayFinder, NamedayFinderLanguage

class ClockDate():
     
     def __init__(self, scale=1.0, language=NamedayFinderLanguage.SK, nameday_json_path="stuff/namesday/nameday.json", position=(20, 20)):
          self.scale = scale
          self.language = language
          self.days_array = ["Po", "Ut", "St", "Št", "Pi", "So", "Ne"]
          self.namedayFinder = NamedayFinder(nameday_json_path)
          self.position = position

     def draw_clock(self, img, position=None, font_path_regular="assets/fonts/raela-grotesque/RaelaGrotesqueRegular-e9476.ttf", font_path_light="assets/fonts/raela-grotesque/RaelaGrotesqueLight-0v1ER.ttf"):
          """
          Vykreslí aktuálny čas, dátum a meniny na zadaný obrázok (PIL.Image).
          :param img: PIL.Image objekt, na ktorý sa má vykresliť
          :param position: tuple (x, y) pozícia pre čas
          :param font_path_regular: cesta k tučnému fontu
          :param font_path_light: cesta k tenkému fontu
          """
          draw = ImageDraw.Draw(img)
          # Určenie pozície
          pos = position if position is not None else self.position

          # Čas
          time_str = datetime.now().strftime("%H:%M")
          font_size_time = int(550 * self.scale)
          timefont = ImageFont.truetype(font_path_regular, font_size_time)
          draw.text(pos, time_str, font=timefont, fill=0)

          # Dátum
          font_size_date = int(200 * self.scale)
          mediumFont = ImageFont.truetype(font_path_light, font_size_date)
          date_str = self.get_date(self.days_array)
          draw.text((pos[0], pos[1] + font_size_time *1.05 * self.scale), date_str, font=mediumFont, fill="#696868")

          # Meniny
          font_size_nameday = int(140 * self.scale)
          smallFont = ImageFont.truetype(font_path_light, font_size_nameday)
          today = datetime.now()
          nameday = self.namedayFinder.find_nameday(today.day, today.month, self.language)
          if nameday:
               nameday_str = f"meniny: {nameday}"
          else:
               nameday_str = ""
          draw.text((pos[0], pos[1] + font_size_time *1.05 * self.scale + font_size_date + 20 * self.scale), nameday_str, font=smallFont, fill="#949492")

     @staticmethod
     def get_date(days_names):
          now = datetime.now()
          day_name = days_names[now.weekday()]
          return f"{day_name}, {now.day}.{now.month}.{now.year}"