# this is main script for weather downloading
# cron runs it in separate process, every 30 minutes?
# actual code runs on non-comercial API

from stuff.parts.weatherservice.weather_fetcher import WeatherFetcher

# Here you put our GPS coordinates
latitude = 49.2231
longitude = 18.7394

fetcher = WeatherFetcher(latitude, longitude)
fetcher.fetch_and_save()
