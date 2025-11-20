import ijson
from typing import Optional, Dict
from enum import Enum
from datetime import datetime


class NamedayFinderLanguage(Enum):
    AT = "at"  # Austria
    BG = "bg"  # Bulgaria
    CZ = "cz"  # Czech Republic
    DE = "de"  # Germany
    DK = "dk"  # Denmark
    EE = "ee"  # Estonia
    ES = "es"  # Spain
    FI = "fi"  # Finland
    FR = "fr"  # France
    GR = "gr"  # Greece
    HR = "hr"  # Croatia
    HU = "hu"  # Hungary
    IT = "it"  # Italy
    LT = "lt"  # Lithuania
    LV = "lv"  # Latvia
    PL = "pl"  # Poland
    RU = "ru"  # Russia
    SE = "se"  # Sweden
    SK = "sk"  # Slovakia
    US = "us"  # United States


class NamedayFinder:
    def __init__(self, json_file_path: str = "assets/namedays_fixed.json"):
        """
        Inicializuje triedu NamedayFinder a nastaví cestu k JSON súboru s meninami.
        :param json_file_path: Cesta k JSON súboru obsahujúcemu meniny (default: assets/namedays_fixed.json).
        """
        self.json_file_path = json_file_path

    def get_nameday_name(self, day: int, month: int, language: NamedayFinderLanguage = NamedayFinderLanguage.SK) -> Optional[str]:
        """
        Vráti meno, ktoré má meniny pre daný deň, mesiac a jazyk z assets/namedays_fixed.json.
        :param day: Deň v mesiaci (1-31)
        :param month: Mesiac (1-12)
        :param language: Jazyková mutácia menín (default: SK).
        :return: Meno ako string, alebo None ak sa nenájde.
        """
        lang_key = language.value
        try:
            with open(self.json_file_path, "r", encoding="utf-8") as f:
                for item in ijson.items(f, 'item'):
                    if item.get('day') == day and item.get('month') == month:
                        return item.get(lang_key, None)
        except Exception:
            return None
        return None



   