from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from forecast.models import (
    Current,
    ForecastDay,
    ForecastHour,
    Astro
)
import datetime
from geo.models import City
from django.contrib.gis.geos import Point
from forecast.controllers import update_weather_info
from miniweather.utils import get_city_from_ip
# Create your views here.


class CurrentWeatherView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Forecast"
        ],
        operation_summary='Get current weather',
        query_serializer=serializers.RequestCurrentWeather
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestCurrentWeather(
            data=request.query_params
        )
        if serializer.is_valid():
            query = None
            if 'lat' in serializer.validated_data and\
               'long' in serializer.validated_data:
                point = Point(
                    x=serializer.validated_data['long'],
                    y=serializer.validated_data['lat'],
                    srid=4326
                )
                query = {
                    'point': point
                }

            elif 'city_id' in serializer.validated_data:
                query = {
                    'id': serializer.validated_data['city_id']
                }
            else:
                city_name = get_city_from_ip(request.headers['X-Real-Ip'])
                if city_name:
                    query = {
                        'name': city_name
                    }

            city = City.find(query)

            if not city:
                update_weather_info(ip=request.headers['X-Real-Ip'])

            if not city or query is None:
                return Response({
                                "message": "Location not found."
                                },
                                status.HTTP_404_NOT_FOUND)
            from_date = datetime.datetime.utcnow()
            from_date -= datetime.timedelta(hours=3)
            current = Current.get(
                city,
                from_date
            )
            astro = Astro.get(
                city,
                date=from_date,
            )
            if not current:
                update_weather_info(city=city)
                current = Current.get(
                    city,
                    from_date
                )
                if not current:
                    return Response({
                        "message": "Weather info not found."
                        },
                        status.HTTP_404_NOT_FOUND)
            current = serializers.ResponseCurrent(
                current
            ).data
            if astro:
                current['astro'] = serializers.ResponseAstro(
                    astro,
                ).data
            else:
                current['astro'] = {}
            return Response(current,
                status.HTTP_200_OK)

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentWeatherListView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Forecast"
        ],
        operation_summary='Get current weather',
        query_serializer=serializers.RequestCurrentWeatherList
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestCurrentWeatherList(
            data=request.query_params
        )
        if serializer.is_valid():
            cities = City.objects.filter(
                id__in=serializer.validated_data['city_ids']
            ).all()

            currents = Current.list(cities)

            return Response({
                    'items': serializers.ResponseCurrent(
                        currents,
                        many=True
                    ).data
                },
                status.HTTP_200_OK)

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ForecastDayView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Forecast"
        ],
        operation_summary='Get current weather',
        query_serializer=serializers.RequestCurrentWeather
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestCurrentWeather(
            data=request.query_params
        )
        if serializer.is_valid():
            query = None

            if 'lat' in serializer.validated_data and\
               'long' in serializer.validated_data:
                point = Point(
                    x=serializer.validated_data['long'],
                    y=serializer.validated_data['lat'],
                    srid=4326
                )
                query = {
                    'point': point
                }

            elif 'city_id' in serializer.validated_data:
                query = {
                    'id': serializer.validated_data['city_id']
                }
            else:
                city_name = get_city_from_ip(request.headers['X-Real-Ip'])
                if city_name:
                    query = {
                        'name': city_name
                    }
            city = City.find(query)
            if not city or query is None:
                return Response({
                                "message": "Location not found."
                                },
                                status.HTTP_404_NOT_FOUND)
            from_date = datetime.datetime.utcnow()
            from_date = from_date.replace(
                hour=23,
                minute=59,
                second=59,
                microsecond=999
            )
            to_date = datetime.datetime.utcnow()
            to_date = to_date.replace(
                hour=23,
                minute=59,
                second=59,
                microsecond=999
            )
            to_date = to_date + datetime.timedelta(days=5)
            forecasts = ForecastDay.list(
                city,
                from_date=from_date,
                to_date=to_date
            )
            return Response(serializers.ResponseForecastDay(
                    forecasts,
                    many=True
                ).data,
                status.HTTP_200_OK)

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ForecastHourView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Forecast"
        ],
        operation_summary='Get current weather',
        query_serializer=serializers.RequestCurrentWeather
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestCurrentWeather(
            data=request.query_params
        )
        if serializer.is_valid():
            query = None

            if 'lat' in serializer.validated_data and\
               'long' in serializer.validated_data:
                point = Point(
                    x=serializer.validated_data['long'],
                    y=serializer.validated_data['lat'],
                    srid=4326
                )
                query = {
                    'point': point
                }

            elif 'city_id' in serializer.validated_data:
                query = {
                    'id': serializer.validated_data['city_id']
                }
            else:
                city_name = get_city_from_ip(request.headers['X-Real-Ip'])
                if city_name:
                    query = {
                        'name': city_name
                    }
            city = City.find(query)
            if not city or query is None:
                return Response({
                                "message": "Location not found."
                                },
                                status.HTTP_404_NOT_FOUND)
            from_date = datetime.datetime.utcnow()
            from_date = from_date.replace(
                hour=23,
                minute=59,
                second=59,
                microsecond=999
            )
            to_date = datetime.datetime.utcnow()
            to_date = to_date.replace(
                hour=23,
                minute=59,
                second=59,
                microsecond=999
            )
            to_date = to_date + datetime.timedelta(days=5)
            forecasts = ForecastHour.list(
                city,
                from_date=from_date,
                to_date=to_date
            )
            return Response(serializers.ResponseForecastHour(
                    forecasts,
                    many=True
                ).data,
                status.HTTP_200_OK)

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class WeatherDetailView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Forecast"
        ],
        operation_summary='Get current weather',
        query_serializer=serializers.RequestCurrentWeather
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestCurrentWeather(
            data=request.query_params
        )
        if serializer.is_valid():
            query = None

            if 'lat' in serializer.validated_data and\
               'long' in serializer.validated_data:
                point = Point(
                    x=serializer.validated_data['long'],
                    y=serializer.validated_data['lat'],
                    srid=4326
                )
                query = {
                    'point': point
                }

            elif 'city_id' in serializer.validated_data:
                query = {
                    'id': serializer.validated_data['city_id']
                }
            else:
                city_name = get_city_from_ip(request.headers['X-Real-Ip'])
                if city_name:
                    query = {
                        'name': city_name
                    }
            city = City.find(query)
            if not city or query is None:
                return Response({
                                "message": "Location not found."
                                },
                                status.HTTP_404_NOT_FOUND)

            from_date = datetime.datetime.utcnow()
            from_date = from_date.replace(
                hour=23,
                minute=59,
                second=59,
                microsecond=999
            )
            to_date = datetime.datetime.utcnow()
            to_date = to_date.replace(
                hour=23,
                minute=59,
                second=59,
                microsecond=999
            )
            to_date = to_date + datetime.timedelta(days=5)

            current = Current.get(
                city
            )
            forecast_days = ForecastDay.list(
                city,
                from_date=from_date,
                to_date=to_date
            )
            forecast_hours = ForecastHour.list(
                city,
                from_date=from_date,
                to_date=to_date
            )
            astros = Astro.list(
                city,
                from_date=from_date,
                to_date=to_date
            )
            return Response({
                    'current': serializers.ResponseCurrent(
                        current
                    ).data,
                    'days': serializers.ResponseForecastDay(
                        forecast_days,
                        many=True
                    ).data,
                    'hours': serializers.ResponseForecastHour(
                        forecast_hours,
                        many=True
                    ).data,
                    'astro': serializers.ResponseAstro(
                        astros,
                        many=True
                    ).data
                },
                status.HTTP_200_OK)

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
