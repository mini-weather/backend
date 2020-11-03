from rest_framework import serializers
from geo.serializers import ResponseCity
from forecast.models import (
    Current,
    ForecastDay,
    ForecastHour,
    Astro
)


class RequestCurrentWeather(serializers.Serializer):
    lat = serializers.FloatField(required=False)
    long = serializers.FloatField(required=False)
    city_id = serializers.IntegerField(required=False)


class RequestCurrentWeatherList(serializers.Serializer):
    city_ids = serializers.ListField(
        child=serializers.IntegerField()
    )


class ResponseCurrent(serializers.ModelSerializer):
    city = ResponseCity()

    class Meta:
        model = Current
        exclude = [
            'id',
            'created_at',
            'modified_at'
        ]


class ResponseForecastDay(serializers.ModelSerializer):
    class Meta:
        model = ForecastDay
        exclude = [
            'id',
            'created_at',
            'modified_at',
            'city'
        ]


class ResponseForecastHour(serializers.ModelSerializer):
    class Meta:
        model = ForecastHour
        exclude = [
            'id',
            'created_at',
            'modified_at',
            'city'
        ]


class ResponseAstro(serializers.ModelSerializer):
    class Meta:
        model = Astro
        exclude = [
            'id',
            'created_at',
            'modified_at',
            'city'
        ]
