from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        'current/list',
        views.CurrentWeatherListView.as_view(),
        name='geo_current'
    ),
    url(
        'current/item',
        views.CurrentWeatherView.as_view(),
        name='geo_current'
    ),
    url(
        'hour',
        views.ForecastHourView.as_view(),
        name='geo_country'
    ),
    url(
        'day',
        views.ForecastDayView.as_view(),
        name='day_viwe'
    ),
    url(
        'detail',
        views.WeatherDetailView.as_view(),
        name='forecast_detail'
    ),
]
