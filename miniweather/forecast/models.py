from django.contrib.gis.db import models
from geo.models import City
# Create your models here.

WIND_DIR_CHOICES = (
    ('N', 'North'),
    ('NbE', 'North by east'),
    ('NNE', 'North-northeast '),
    ('NEbN', 'Northeast by north'),
    ('NE', 'Northeast'),
    ('NEbE', 'Northeast by east'),
    ('ENE', 'East-northeast'),
    ('EbN', 'East by north'),
    ('E', 'East'),
    ('EbS', 'East by south'),
    ('ESE', 'East-southeast'),
    ('SEbE', 'Southeast by east'),
    ('SE', 'Southeast'),
    ('SEbS', 'Southeast by south'),
    ('SSE', 'South-southeast'),
    ('SbE', 'South by east'),
    ('S', 'South'),
    ('SbW', 'South by west'),
    ('SSW', 'South-southwest'),
    ('SWbS', 'Southwest by south'),
    ('SW', 'Southwest'),
    ('SWbW', 'Southwest by west'),
    ('WSW', 'West-southwest'),
    ('WbS', 'West by south'),
    ('W', 'West'),
    ('WbN', 'West by north'),
    ('WNW', 'West-northwest'),
    ('NWbW', 'Northwest by west'),
    ('NW', 'Northwest'),
    ('NWbN', 'Northwest by north'),
    ('NNW', 'North-northwest'),
    ('NbW', 'North by west'),
)

MOON_PHASE_CHOICES = (
    ('new_moon', 'New Moon'),
    ('waxing_crescent', 'Waxing Crescent'),
    ('first_quarter', 'First Quarter'),
    ('waxing_gibbous', 'Waxing Gibbous'),
    ('full_moon', 'Full Moon'),
    ('waning_gibbous', 'Waning Gibbous'),
    ('last_quarter', 'Last Quarter'),
    ('waning_crescent', 'Waning Crescent'),
)


class Current(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='city_current'
    )
    last_update = models.DateTimeField(
        null=False, blank=False
    )
    temp_c = models.FloatField(
        null=False, blank=False
    )
    temp_f = models.FloatField(
        null=False, blank=False
    )
    feelslike_c = models.FloatField(
        null=False, blank=False,
    )
    feelslike_f = models.FloatField(
        null=False, blank=False,
    )
    is_day = models.BooleanField(
        null=False, blank=False
    )
    condition = models.IntegerField(
        null=False, blank=False
    )
    wind_mph = models.FloatField(
        null=False, blank=False,
        default=0
    )
    wind_kph = models.FloatField(
        null=False, blank=False,
        default=0
    )
    wind_degree = models.IntegerField(
        null=False, blank=False,
        default=0
    )
    wind_dir = models.CharField(
        max_length=5,
        null=False, blank=False,
        choices=WIND_DIR_CHOICES
    )
    pressure_mb = models.FloatField(
        null=False, blank=False,
        default=0
    )
    pressure_in = models.FloatField(
        null=False, blank=False,
        default=0
    )
    precip_mm = models.FloatField(
        null=False, blank=False,
        default=0
    )
    precip_in = models.FloatField(
        null=False, blank=False,
        default=0
    )
    humidity = models.IntegerField(
        null=False, blank=False,
        default=0
    )
    cloud = models.BooleanField(
        null=False, blank=False,
        default=0
    )
    vis_km = models.FloatField(
        null=False, blank=False,
    )
    vis_miles = models.FloatField(
        null=False, blank=False,
    )
    uv = models.FloatField(
        null=False, blank=False,
    )
    gust_mph = models.FloatField(
        null=False, blank=False,
    )
    gust_kph = models.FloatField(
        null=False, blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
    )

    @classmethod
    def get(cls, city, date=None):
        obj = cls.objects.filter(city=city)
        if date:
            obj = obj.filter(last_update__gte=date)
        return obj.first()

    @classmethod
    def list(cls, cities, date=None):
        obj = cls.objects.filter(
            city__in=cities
        )
        if date:
            obj = obj.filter(last_update__gte=date)
        return obj.distinct('city').all()

    @classmethod
    def upsert(cls, data, city, last_update):
        obj = cls.objects.filter(
            city=city,
            last_update=last_update
        ).first()

        if not obj:
            obj = cls(
            city=city,
            last_update=last_update
        )

        obj.temp_c = data['temp_c']
        obj.temp_f = data['temp_f']
        obj.feelslike_c = data['feelslike_c']
        obj.feelslike_f = data['feelslike_f']
        obj.is_day = True if data['is_day'] == 1 else False
        obj.condition = data['condition']['code']
        obj.wind_mph = data['wind_mph']
        obj.wind_kph = data['wind_kph']
        obj.wind_degree = data['wind_degree']
        obj.wind_dir = data['wind_dir']
        obj.pressure_mb = data['pressure_mb']
        obj.pressure_in = data['pressure_in']
        obj.precip_mm = data['precip_mm']
        obj.precip_in = data['precip_in']
        obj.humidity = data['humidity']
        obj.cloud = True if data['cloud'] == 1 else False
        obj.vis_km = data['vis_km']
        obj.vis_miles = data['vis_miles']
        obj.uv = data['uv']
        obj.gust_mph = data['gust_mph']
        obj.gust_kph = data['gust_kph']
        obj.save()

        return obj

class ForecastDay(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='city_forecast_day'
    )
    date = models.DateField(
        null=False,
        blank=False
    )
    maxtemp_c = models.FloatField(
        null=False, blank=False
    )
    maxtemp_f = models.FloatField(
        null=False, blank=False
    )
    mintemp_c = models.FloatField(
        null=False, blank=False,
    )
    mintemp_f = models.FloatField(
        null=False, blank=False,
    )
    avgtemp_c = models.FloatField(
        null=False, blank=False,
    )
    avgtemp_f = models.FloatField(
        null=False, blank=False,
    )
    condition = models.IntegerField(
        null=False, blank=False
    )
    uv = models.FloatField(
        null=False, blank=False,
    )
    maxwind_mph = models.FloatField(
        null=False, blank=False
    )
    maxwind_kph = models.FloatField(
        null=False, blank=False
    )
    totalprecip_mm = models.FloatField(
        null=False, blank=False,
    )
    totalprecip_in = models.FloatField(
        null=False, blank=False,
    )
    avgvis_miles = models.FloatField(
        null=False, blank=False,
    )
    avgvis_km = models.FloatField(
        null=False, blank=False,
    )

    avghumidity = models.FloatField(
        null=False, blank=False,
    )

    daily_will_it_rain = models.BooleanField(
        null=False, blank=False,
        default=False
    )

    daily_chance_of_rain = models.IntegerField(
        null=False, blank=False,
        default=0
    )

    daily_will_it_snow = models.BooleanField(
        null=False, blank=False,
        default=False
    )

    daily_chance_of_snow = models.IntegerField(
        null=False, blank=False,
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
    )

    @classmethod
    def list(cls, city, date=None, from_date=None, to_date=None):
        obj = cls.objects.filter(city=city)
        if date:
            obj = obj.filter(date=date)
        if from_date:
            obj = obj.filter(date__gte=from_date)
        if to_date:
            obj = obj.filter(date__lte=to_date)
        return obj.all()

    @classmethod
    def upsert(cls, data, city, date):
        obj = cls.objects.filter(
            city=city,
            date=date
        ).first()

        if not obj:
            obj = cls(
            city=city,
            date=date
        )

        obj.maxtemp_c = data['maxtemp_c']
        obj.maxtemp_f = data['maxtemp_f']
        obj.mintemp_c = data['mintemp_c']
        obj.mintemp_f = data['mintemp_f']
        obj.avgtemp_c = data['avgtemp_c']
        obj.avgtemp_f = data['avgtemp_f']
        obj.condition = data['condition']['code']
        obj.uv = data['uv']
        obj.maxwind_mph = data['maxwind_mph']
        obj.maxwind_kph = data['maxwind_kph']
        obj.totalprecip_mm = data['totalprecip_mm']
        obj.totalprecip_in = data['totalprecip_in']
        obj.avgvis_miles = data['avgvis_miles']
        obj.avgvis_km = data['avgvis_km']
        obj.avghumidity = data['avghumidity']

        obj.daily_will_it_rain = True if data[
            'daily_will_it_rain'
        ] == 1 else False
        obj.daily_chance_of_rain = data['daily_chance_of_rain']

        obj.daily_will_it_snow = True if data[
            'daily_will_it_snow'
        ] == 1 else False
        obj.daily_chance_of_snow = data['daily_chance_of_snow']
        obj.save()

        return obj


class ForecastHour(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='city_forecast_hour'
    )
    date_time = models.DateTimeField(
        null=False,
        blank=False
    )

    temp_c = models.FloatField(
        null=False, blank=False
    )
    temp_f = models.FloatField(
        null=False, blank=False
    )
    feelslike_c = models.FloatField(
        null=False, blank=False,
    )
    feelslike_f = models.FloatField(
        null=False, blank=False,
    )
    is_day = models.BooleanField(
        null=False, blank=False
    )
    condition = models.IntegerField(
        null=False, blank=False
    )
    wind_mph = models.FloatField(
        null=False, blank=False,
        default=0
    )
    wind_kph = models.FloatField(
        null=False, blank=False,
        default=0
    )
    wind_degree = models.IntegerField(
        null=False, blank=False,
        default=0
    )
    wind_dir = models.CharField(
        max_length=5,
        null=False, blank=False,
        choices=WIND_DIR_CHOICES
    )
    pressure_mb = models.FloatField(
        null=False, blank=False,
        default=0
    )
    pressure_in = models.FloatField(
        null=False, blank=False,
        default=0
    )
    precip_mm = models.FloatField(
        null=False, blank=False,
        default=0
    )
    precip_in = models.FloatField(
        null=False, blank=False,
        default=0
    )
    humidity = models.IntegerField(
        null=False, blank=False,
        default=0
    )
    cloud = models.BooleanField(
        null=False, blank=False,
        default=0
    )
    windchill_c = models.FloatField(
        null=False, blank=False,
        default=0
    )
    windchill_f = models.FloatField(
        null=False, blank=False,
        default=0
    )
    heatindex_c = models.FloatField(
        null=False, blank=False,
        default=0
    )
    heatindex_f = models.FloatField(
        null=False, blank=False,
        default=0
    )
    dewpoint_c = models.FloatField(
        null=False, blank=False,
        default=0
    )
    dewpoint_f = models.FloatField(
        null=False, blank=False,
        default=0
    )
    vis_km = models.FloatField(
        null=False, blank=False,
    )
    vis_miles = models.FloatField(
        null=False, blank=False,
    )
    gust_mph = models.FloatField(
        null=False, blank=False,
    )
    gust_kph = models.FloatField(
        null=False, blank=False,
    )
    will_it_rain = models.BooleanField(
        null=False, blank=False,
        default=False
    )

    chance_of_rain = models.IntegerField(
        null=False, blank=False,
        default=0
    )

    will_it_snow = models.BooleanField(
        null=False, blank=False,
        default=False
    )

    chance_of_snow = models.IntegerField(
        null=False, blank=False,
        default=0
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
    )

    @classmethod
    def list(cls, city, from_date=None, to_date=None):
        obj = cls.objects.filter(city=city)
        if from_date:
            obj = obj.filter(date_time__gte=from_date)
        if to_date:
            obj = obj.filter(date_time__lte=to_date)
        return obj.all()

    @classmethod
    def upsert(cls, data, city, date_time):
        obj = cls.objects.filter(
            city=city,
            date_time=date_time
        ).first()

        if not obj:
            obj = cls(
            city=city,
            date_time=date_time
        )

        obj.temp_c = data['temp_c']
        obj.temp_f = data['temp_f']
        obj.feelslike_c = data['feelslike_c']
        obj.feelslike_f = data['feelslike_f']
        obj.is_day = True if data['is_day'] == 1 else False
        obj.condition = data['condition']['code']
        obj.wind_mph = data['wind_mph']
        obj.wind_kph = data['wind_kph']
        obj.wind_degree = data['wind_degree']
        obj.wind_dir = data['wind_dir']
        obj.pressure_mb = data['pressure_mb']
        obj.pressure_in = data['pressure_in']
        obj.precip_mm = data['precip_mm']
        obj.precip_in = data['precip_in']
        obj.humidity = data['humidity']
        obj.cloud = True if data['cloud'] == 1 else False
        
        obj.windchill_c = data['windchill_c']
        obj.windchill_f = data['windchill_f']

        obj.heatindex_c = data['heatindex_c']
        obj.heatindex_f = data['heatindex_f']

        obj.dewpoint_c = data['dewpoint_c']
        obj.dewpoint_f = data['dewpoint_f']

        obj.vis_km = data['vis_km']
        obj.vis_miles = data['vis_miles']
        obj.gust_mph = data['gust_mph']
        obj.gust_kph = data['gust_kph']

        obj.will_it_rain = True if data[
            'will_it_rain'
        ] == 1 else False
        obj.chance_of_rain = data['chance_of_rain']

        obj.will_it_snow = True if data[
            'will_it_snow'
        ] == 1 else False
        obj.chance_of_snow = data['chance_of_snow']

        obj.save()

        return obj


class Astro(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='city_astro'
    )
    date = models.DateField(
        null=False,
        blank=False
    )
    moon_phase = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        choices=MOON_PHASE_CHOICES
    )
    moon_illumination = models.IntegerField(
        null=False,
        blank=False,
        default=0
    )
    sunrise = models.TimeField(
        null=False,
        blank=False,
    )
    sunset = models.TimeField(
        null=False,
        blank=False,
    )
    moonrise = models.TimeField(
        null=False,
        blank=False,
    )
    moonset = models.TimeField(
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        null=False,
        blank=False
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        null=False,
        blank=False
    )

    @classmethod
    def get(cls, city, date=None, from_date=None, to_date=None):
        obj = cls.objects.filter(city=city)
        if date:
            obj = obj.filter(date=date)
        if from_date:
            obj = obj.filter(date__gte=from_date)
        if to_date:
            obj = obj.filter(date__lte=to_date)
        return obj.first()

    @classmethod
    def list(cls, city, date=None, from_date=None, to_date=None):
        obj = cls.objects.filter(city=city)
        if date:
            obj = obj.filter(date=date)
        if from_date:
            obj = obj.filter(date__gte=from_date)
        if to_date:
            obj = obj.filter(date__lte=to_date)
        return obj.all()