from django.core.management.base import BaseCommand
import json
from geo.models import Country, Province
from django.contrib.gis.geos import GEOSGeometry, fromstr, MultiPolygon


class Command(BaseCommand):
    help = "Update Provinces"

    def handle(self, *args, **kwargs):
        with open('geo/data/states.geojson') as json_file:
            data = json.load(json_file)
            for feature in data['features']:
                country_name = feature['properties']['NAME_0']
                province_name = feature['properties']['NAME_1']
                print(country_name)
                print(province_name)
                country = Country.objects.filter(name=country_name).first()
                if not country:
                    country = Country(
                        name=country_name
                    )
                    country.save()

                province = Province.objects.filter(
                    name=province_name,
                    country=country).first()

                if not province:
                    province = Province(
                        name=province_name,
                        country=country
                    )
                    province.save()
                geom = GEOSGeometry(str(feature['geometry']))
                if (feature['geometry']['type'] == 'Polygon'):
                    geom = MultiPolygon(fromstr(str(geom)),)

                province.area = geom
                province.save()
