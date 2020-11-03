from django.core.management.base import BaseCommand
import json
from geo.models import Country, Province, City
from django.contrib.gis.geos import GEOSGeometry, fromstr, MultiPolygon


class Command(BaseCommand):
    help = "Update Provinces"

    def handle(self, *args, **kwargs):
        with open('geo/data/all_cities.geojson') as json_file:
            data = json.load(json_file)
            for feature in data['features']:
                if 'NAME' not in feature['properties']:
                    continue
                city_name = feature['properties']['NAME']
                geom = GEOSGeometry(str(feature['geometry']))
                if (feature['geometry']['type'] == 'Polygon'):
                    geom = MultiPolygon(fromstr(str(geom)))

                # if City.objects.filter(
                #     center__coveredby=geom
                # ).count() > 1:
                #     print(city_name)
                #     for city in City.objects.filter(
                #         center__coveredby=geom
                #     ).all():
                #         print(city.name)
                #         print(city.id)
                #         print('........................')
                #     print("####################")

                city = City.objects.filter(
                    center__coveredby=geom
                ).first()
                if city:
                    city.area = geom
                    city.save()
