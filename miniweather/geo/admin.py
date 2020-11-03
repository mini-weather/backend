from django.contrib.gis import admin
from .models import Country, Province, City
from leaflet.admin import LeafletGeoAdmin
# Register your models here.


@admin.register(Country)
class CountryAdmin(LeafletGeoAdmin):
    search_fields = ['name', ]
    list_display = [
                    "id",
                    "name",
                  ]


@admin.register(Province)
class ProvinceAdmin(LeafletGeoAdmin):
    search_fields = ['name', 'country__name']
    list_display = [
                    "id",
                    "name",
                    "country"
                ]


@admin.register(City)
class CityAdmin(LeafletGeoAdmin):
    search_fields = ['name', 'province__name']
    list_display = [
                    "id",
                    "name",
                    "province"
                ]
