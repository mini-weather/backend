from rest_framework import serializers
from .models import Country, Province, City


class RequestCurrentGet(serializers.Serializer):
    lat = serializers.FloatField(required=True)
    long = serializers.FloatField(required=True)


class RequestGeoCountryGet(serializers.Serializer):
    query = serializers.CharField(required=False, min_length=3)


class RequestGeoProvinceGet(serializers.Serializer):
    query = serializers.CharField(required=False, min_length=3)
    country_id = serializers.IntegerField(required=True)


class RequestGeoCityGet(serializers.Serializer):
    query = serializers.CharField(required=False, min_length=3)
    province_id = serializers.IntegerField(required=True)


class ResponseCountry(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = [
            "currencies",
            "area_units",
            "name",
            "id"
        ]


class ResponseProvince(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = [
            "name",
            "id"
        ]


class ResponseCity(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "name",
            "time_zone",
            "id"
        ]


class ResponseCityFull(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "name",
            "id",
            "area"
        ]
