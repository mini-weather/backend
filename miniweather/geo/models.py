from django.contrib.gis.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=100)
    area = models.MultiPolygonField(null=True, blank=True)
    code = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_list(cls, data):
        query = {}
        if 'query' in data:
            if data['query'] and len(data['query']) < 3:
                return []
            query['name__icontains'] = data['query']
        countries = Country.objects.filter(**query).all()
        return countries

    @classmethod
    def find(cls, data):
        query = {}
        if 'point' in data:
            query['point__contains'] = data['point']
        else:
            if 'name' in data:
                query['name'] = data['name']
        country = Country.objects.filter(**query).first()
        return country


class Province(models.Model):
    name = models.CharField(max_length=100)
    area = models.MultiPolygonField(null=True, blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='province'
    )

    def __str__(self):
        return self.name

    @classmethod
    def get_list(cls, data):
        query = {
            'country_id': data['country_id']
        }
        if 'query' in data:
            if data['query'] and len(data['query']) < 3:
                return []
            query['name__icontains'] = data['query']
        provnices = Province.objects.filter(**query).all()
        return provnices

    @classmethod
    def find(cls, data):
        query = {}
        if 'point' in data:
            query['point__contains'] = data['point']
        else:
            if 'name' in data:
                query['name__iexact'] = data['name']
            if 'country_id' in data:
                query['country_id'] = data['country_id']
        provnice = Province.objects.filter(**query).first()
        return provnice


class City(models.Model):
    name = models.CharField(max_length=100)
    area = models.MultiPolygonField(null=True, blank=True)
    center = models.PointField(null=True, blank=True)
    time_zone = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        related_name='city',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

    @classmethod
    def add(cls, data):
        obj = City()
        if 'name' in data:
            obj.name = data['name'].lower()
        if 'time_zone' in data:
            obj.time_zone = data['time_zone']
        if 'province' in data:
            obj.province = data['province']
        obj.save()
        return obj

    @classmethod
    def get_list(cls, data):
        query = {
            'province_id': data['province_id']
        }
        if 'query' in data:
            if data['query'] and len(data['query']) < 3:
                return []
            query['name__icontains'] = data['query']
        cities = City.objects.filter(**query).all()
        return cities

    @classmethod
    def find(cls, data):
        if not data:
            return None
        query = {}
        if 'id' in data:
            return City.objects.filter(id=data['id']).first()
        if 'point' in data:
            query['area__contains'] = data['point']
        else:
            if 'name' in data:
                query['name__iexact'] = data['name']
            if 'province_id' in data:
                query['province_id'] = data['province_id']
        city = City.objects.filter(**query).first()
        return city
