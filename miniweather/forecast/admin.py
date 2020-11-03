from django.contrib.gis import admin
from .models import Current, ForecastDay, ForecastHour, Astro
from leaflet.admin import LeafletGeoAdmin
# Register your models here.


@admin.register(Current)
class CurrentAdmin(LeafletGeoAdmin):
    autocomplete_fields = [
        'city'
    ]

@admin.register(ForecastDay)
class ForecastDayAdmin(LeafletGeoAdmin):
    autocomplete_fields = [
        'city'
    ]

@admin.register(ForecastHour)
class ForecastHourAdmin(LeafletGeoAdmin):
    autocomplete_fields = [
        'city'
    ]

@admin.register(Astro)
class AstroAdmin(LeafletGeoAdmin):
    autocomplete_fields = [
        'city'
    ]
