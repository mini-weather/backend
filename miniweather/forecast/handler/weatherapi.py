from django.conf import settings
import requests

BASE_URL = 'https://api.weatherapi.com/v1'

class WeatherApi:
    
    def get_realtime(city):
        url =  '%s/current.json?key=%s&q=%s' % (
            BASE_URL,
            settings.WEATHER_API_TOKEN,
            city
        )
        result = requests.get(url)
        try:
            return result.json()
        except Exception as e:
            return None

    def get_forecast(city, days=10):
        url =  '%s/forecast.json?key=%s&q=%s&days=%d' % (
            BASE_URL,
            settings.WEATHER_API_TOKEN,
            city,
            days
        )
        result = requests.get(url)
        try:
            return result.json()
        except Exception as e:
            return None