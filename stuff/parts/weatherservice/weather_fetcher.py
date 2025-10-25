import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import json

class WeatherFetcher:
    def __init__(self, latitude, longitude, export_path="export/weather-actual.json"):
        self.latitude = latitude
        self.longitude = longitude
        self.export_path = export_path
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)

    def fetch_and_save(self):
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current": ["temperature_2m", "apparent_temperature", "precipitation", "weather_code"],
            "forecast_days": 1,
            "timezone": "Europe/Berlin"
        }
        responses = self.openmeteo.weather_api(url, params=params)
        response = responses[0]

        # Extract current weather
        current = response.Current()
        current_data = {
            "time": current.Time(),
            "temperature_2m": current.Variables(0).Value(),
            "apparent_temperature": current.Variables(1).Value(),
            "precipitation": current.Variables(2).Value(),
            "weather_code": current.Variables(3).Value()
        }

        # Save only current data to JSON
        export = {
            "current": current_data
        }
        with open(self.export_path, "w", encoding="utf-8") as f:
            json.dump(export, f, ensure_ascii=False, indent=2)
