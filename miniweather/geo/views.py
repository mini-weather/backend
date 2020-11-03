from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from drf_yasg.utils import swagger_auto_schema
from .models import Country, Province, City
from django.contrib.gis.geos import Point
# Create your views here.


class GeoCurrentView(APIView):

    @swagger_auto_schema(
        responses={
            200: {}
        },
        tags=[
            "Geo"
        ],
        operation_summary='Get current location info',
        query_serializer=serializers.RequestCurrentGet
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestCurrentGet(
            data=request.query_params
        )
        if serializer.is_valid():
            point = Point(
                x=serializer.validated_data['long'],
                y=serializer.validated_data['lat'],
                srid=4326
            )
            city = City.find(
                {
                    'point': point
                }
            )
            if not city:
                return Response({
                                "message": "Location not found."
                                },
                                status.HTTP_404_NOT_FOUND)
            return Response({
                    "city": serializers.ResponseCity(
                        city
                    ).data,
                    "province": serializers.ResponseProvince(
                        city.province
                    ).data,
                    "country": serializers.ResponseCountry(
                        city.province.country
                    ).data,

                },
                status.HTTP_200_OK)

        else:
            return Response(
                {
                    "message": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class GeoCountryListView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseCountry(many=True)
        },
        tags=[
            "Geo"
        ],
        operation_summary='Get country list',
        query_serializer=serializers.RequestGeoCountryGet
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestGeoCountryGet(
            data=request.query_params
        )
        if serializer.is_valid():
            countries = Country.get_list(serializer.validated_data)

            return Response(serializers.ResponseCountry(
                    countries,
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


class GeoProvinceListView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseProvince(many=True)
        },
        tags=[
            "Geo"
        ],
        operation_summary='Get province list',
        query_serializer=serializers.RequestGeoProvinceGet
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestGeoProvinceGet(
            data=request.query_params
        )
        if serializer.is_valid():
            provinces = Province.get_list(serializer.validated_data)

            return Response(serializers.ResponseProvince(
                    provinces,
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


class GeoCityListView(APIView):

    @swagger_auto_schema(
        responses={
            200: serializers.ResponseCity(many=True)
        },
        tags=[
            "Geo"
        ],
        operation_summary='Get city list',
        query_serializer=serializers.RequestGeoCityGet
    )
    def get(self, request, *args, **kwargs):
        serializer = serializers.RequestGeoCityGet(
            data=request.query_params
        )
        if serializer.is_valid():
            cities = City.get_list(serializer.validated_data)

            return Response(serializers.ResponseCity(
                    cities,
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
