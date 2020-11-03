from django.core.management.base import BaseCommand
from forecast.controllers import update_weather_info
from geo.models import City

class Command(BaseCommand):
    help = "Test Weather API"

    def handle(self, *args, **kwargs):
        city = City.objects.filter(name='tehran').first()
        update_weather_info(city)
