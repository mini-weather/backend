from django.core.management.base import BaseCommand
import json
from geo.models import Country, Province, City
from django.contrib.gis.geos import Point
import unidecode


class Command(BaseCommand):
    help = "Update Provinces"

    def handle(self, *args, **kwargs):
        with open('geo/data/cities_data.json') as json_file:
            data = json.load(json_file)
            for country_data in data:
                # if country_data['name'] not in ['Iran', 'Germany', 'Sweden']:
                #     continue
                country_data['name'] = unidecode.unidecode(
                    country_data['name'].lower()
                )
                country = Country.objects.filter(
                    name=country_data['name']
                ).first()
                if not country:
                    country = Country(
                        name=country_data['name'],
                        code=country_data['iso2']
                    )
                    country.save()
                for province_data in country_data['states']:
                     
                    if province_data['name'].endswith(' District'):
                        province_data['name'] = province_data['name'].replace(
                            ' District', ''
                        )
                    if province_data['name'].endswith(' Province'):
                        province_data['name'] = province_data['name'].replace(
                            ' Province', ''
                        )
                    if province_data['name'].endswith(' County'):
                        province_data['name'] = province_data['name'].replace(
                            ' County', ''
                        )
                    province_data['name'] = unidecode.unidecode(
                        province_data['name'].lower()
                    )
                    province = Province.objects.filter(
                        name=province_data['name'],
                        country=country
                    ).first()
                    if not province:
                        province = Province(
                            name=province_data['name'],
                            country=country
                        )
                        province.save()
                    for city_data in province_data['cities']:
                        if city_data['name'].startswith('Shahrestān-e '):
                            city_data['name'] = city_data['name'].replace(
                                'Shahrestān-e ', ''
                            )
                        if city_data['name'].endswith(' District'):
                            city_data['name'] = city_data['name'].replace(
                                ' District', ''
                            )
                        city_data['name'] = unidecode.unidecode(
                            city_data['name'].lower()
                        )
                        city = City.objects.filter(
                            name=city_data['name'],
                            province=province
                        ).first()
                        if not city:
                            city = City(
                                name=city_data['name'],
                                province=province
                            )
                        city.center = Point(
                            x=float(city_data['longitude']),
                            y=float(city_data['latitude']),
                            srid=4326
                        )
                        city.save()
