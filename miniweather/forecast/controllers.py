from forecast.handler.weatherapi import WeatherApi
from forecast.models import (
    Current,
    ForecastDay,
    ForecastHour,
    Astro
)
from geo.models import City
import datetime
import pytz
from django.core.cache import cache
from django.conf import settings


def update_weather_info(city=None, ip=None):
    result = None
    if city is not None:
        result = WeatherApi.get_forecast('%f,%f' % (
                city.center.y, city.center.x
            )
        )
    elif ip is not None:
        result = WeatherApi.get_forecast(ip)

    if not result:
        return

    if city is None:
        city = City.find({
            'name': result['location']['name'].lower()
        })
        cache.set("location_ip:%s" % (
                ip
            ),
            result['location']['name'].lower(),
            timeout=settings.IP2LOCATION_TTL
        )
        if not city:
            city = City.add({
                'name': result['location']['name']
            })
            

    time_zone = result['location']['tz_id']
    local_tz = pytz.timezone(time_zone)
    if time_zone:
        city.time_zone = time_zone
        city.save()

    native = datetime.datetime.strptime(
        result['current']['last_updated'],
        "%Y-%m-%d %H:%M"
    )
    local_dt = local_tz.localize(native, is_dst=None)
    last_update = local_dt.astimezone(pytz.utc)
    
    Current.upsert(
        result['current'],
        city,
        last_update
    )

    if 'forecast' in result and 'forecastday' in result['forecast']:
        for forecast in result['forecast']['forecastday']:
            date = forecast['date']
            if 'day' in forecast:
                ForecastDay.upsert(
                    forecast['day'],
                    city,
                    date
                )
            if 'hour' in forecast:
                for hour in forecast['hour']:
                    native = datetime.datetime.strptime(
                        hour['time'],
                        "%Y-%m-%d %H:%M"
                    )
                    local_dt = local_tz.localize(native, is_dst=None)
                    time = local_dt.astimezone(pytz.utc)
                    ForecastHour.upsert(
                        hour,
                        city,
                        time
                    )

            if 'astro' in forecast:
                astro = Astro.objects.filter(
                    city=city,
                    date=date
                ).first()

                if not astro:
                    astro = Astro(
                        city=city,
                        date=date
                    )
                sunrise = datetime.datetime.strptime(
                    forecast['astro']['sunrise'],
                    '%I:%M %p'
                )
                sunrise = local_tz.localize(sunrise, is_dst=None)
                sunrise = sunrise.astimezone(pytz.utc)

                sunset = datetime.datetime.strptime(
                    forecast['astro']['sunset'],
                    '%I:%M %p'
                )
                sunset = local_tz.localize(sunset, is_dst=None)
                sunset = sunset.astimezone(pytz.utc)

                moonrise = datetime.datetime.strptime(
                    forecast['astro']['moonrise'],
                    '%I:%M %p'
                )
                moonrise = local_tz.localize(moonrise, is_dst=None)
                moonrise = moonrise.astimezone(pytz.utc)

                moonset = datetime.datetime.strptime(
                    forecast['astro']['moonset'],
                    '%I:%M %p'
                )
                moonset = local_tz.localize(moonset, is_dst=None)
                moonset = moonset.astimezone(pytz.utc)

                moon_illumination = int(
                    forecast['astro']['moon_illumination']
                )
                moon_phase = forecast['astro']['moon_phase'].lower()
                moon_phase = moon_phase.replace(' ', '_')

                astro.sunrise = sunrise
                astro.sunset = sunset
                astro.moonrise = moonrise
                astro.moonset = moonset
                astro.moon_illumination = moon_illumination
                astro.moon_phase = moon_phase


                astro.save()