import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import json

class WeatherFetcher:
    def __init__(self, latitude, longitude, export_path="assets/weather-actual.json"):
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
            "hourly": [
                "temperature_2m", "precipitation_probability",
                "precipitation", "pressure_msl"
            ],
            "forecast_days": 4,
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

        # Extract hourly data
        hourly = response.Hourly()
        # Store 'time' as provided by the API (array of ISO strings)
        times = hourly.Time()
        if isinstance(times, list):
            time_list = times
        else:
            time_list = [times]
        hourly_data = {
            "time": time_list,
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy().tolist(),
            "precipitation_probability": hourly.Variables(1).ValuesAsNumpy().tolist(),
            "precipitation": hourly.Variables(2).ValuesAsNumpy().tolist(),
            "pressure_msl": hourly.Variables(3).ValuesAsNumpy().tolist()
        }

        # Add previous hour forecast (last value from hourly arrays)
        previous_hour = {
            "precipitation": hourly_data["precipitation"][-2] if len(hourly_data["precipitation"]) > 1 else None,
            "precipitation_probability": hourly_data["precipitation_probability"][-2] if len(hourly_data["precipitation_probability"]) > 1 else None
        }

        export = {
            "current": current_data,
            "hourly": hourly_data,
            "previous_hour": previous_hour
        }
        with open(self.export_path, "w", encoding="utf-8") as f:
            json.dump(export, f, ensure_ascii=False, indent=2)
