import json
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
    def __init__(self, json_file_path: str):
        """
        Inicializuje triedu NamedayFinder a načíta JSON súbor.

        :param json_file_path: Cesta k JSON súboru obsahujúcemu meniny.
        """
        self.json_file_path = json_file_path
        self.nameday_data = self._load_json()

    def _load_json(self) -> list:
        """
        Načíta JSON súbor a vráti jeho obsah ako zoznam.

        :return: Zoznam záznamov z JSON súboru.
        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Chyba: Súbor {self.json_file_path} neexistuje.")
            return []
        except json.JSONDecodeError:
            print(f"Chyba: Súbor {self.json_file_path} nie je platný JSON.")
            return []

    def find_nameday(self, day: int, month: int, language: NamedayFinderLanguage) -> Optional[str]:
        """
        Vyhľadá meniny na základe zadaného dňa, mesiaca, roku a jazyka.

        :param day: Deň, ktorý sa má vyhľadať.
        :param month: Mesiac, ktorý sa má vyhľadať.
        :param year: Rok, ktorý sa má vyhľadať (aktuálne sa nepoužíva, ale môže byť rozšírený).
        :param language: Jazyk, v ktorom sa má vyhľadať meniny (napr. "sk", "us").
        :return: Meniny ako reťazec, alebo None, ak sa nenašli.
        """
        for record in self.nameday_data:
            if record.get("day") == day and record.get("month") == month:
                return record.get(language.value, None)
        return None
    
    def today_nameday(self, language: NamedayFinderLanguage) -> Optional[str]:
        """
        Zobrazí meniny aktuálneho dňa podľa systémového času a zadaného jazyka.

        :param language: Jazyk, v ktorom sa má vyhľadať meniny (napr. "sk", "us").
        :return: Meniny ako reťazec, alebo None, ak sa nenašli.
        """
        today = datetime.now()
        return self.find_nameday(today.day, today.month, today.year, language)


