from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        'current',
        views.GeoCurrentView.as_view(),
        name='geo_current'
    ),
    url(
        'country/list',
        views.GeoCountryListView.as_view(),
        name='geo_country'
    ),
    url(
        'province/list',
        views.GeoProvinceListView.as_view(),
        name='geo_province'
    ),
    url(
        'city/list',
        views.GeoCityListView.as_view(),
        name='geo_city'
    ),
]
