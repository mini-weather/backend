from django.core.management.base import BaseCommand
import json
from geo.models import Country
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, fromstr


class Command(BaseCommand):
    help = "Update Countries"

    def handle(self, *args, **kwargs):
        with open('geo/data/countries.geojson') as json_file:
            data = json.load(json_file)
            for feature in data['features']:
                country_name = feature['properties']['ADMIN']
                print(country_name)
                country = Country.objects.filter(name=country_name).first()
                if not country:
                    country = Country(
                        name=country_name
                    )
                    country.save()
                geom = GEOSGeometry(str(feature['geometry']))
                if (feature['geometry']['type'] == 'Polygon'):
                    geom = MultiPolygon(fromstr(str(geom)),)
                country.area = geom
                country.save()
