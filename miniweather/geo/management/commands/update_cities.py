from django.core.management.base import BaseCommand
import json
from geo.models import Country, Province, City
from django.contrib.gis.geos import GEOSGeometry, fromstr, MultiPolygon


class Command(BaseCommand):
    help = "Update Provinces"

    def handle(self, *args, **kwargs):
        with open('geo/data/cities.geojson') as json_file:
            data = json.load(json_file)
            for feature in data['features']:
                print(feature['properties'])
                if 'NAME_2' not in feature['properties']:
                    continue
                country_name = feature['properties']['NAME_0']
                province_name = feature['properties']['NAME_1']
                city_name = feature['properties']['NAME_2']

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
                    print(province_name)
                    print(city_name)
                    print('#########################')
                    continue

                city = City.objects.filter(
                    name=city_name,
                    province=province
                ).first()

                if not city:
                    city = City(
                        name=city_name,
                        province=province
                    )
                    city.save()

                geom = GEOSGeometry(str(feature['geometry']))
                if (feature['geometry']['type'] == 'Polygon'):
                    geom = MultiPolygon(fromstr(str(geom)),)

                city.area = geom
                city.save()
