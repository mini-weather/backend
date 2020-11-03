import IP2Location
from django.core.cache import cache
from django.conf import settings

IP2Loc = IP2Location.IP2Location()
IP2Loc.open(
    './data/ip2location.bin'
)


def get_city_from_ip(ip):
    if ip == '127.0.0.1':
        return 'tehran'
    city = cache.get("location_ip:%s" % (
            ip
        )
    )
    if city:
        return city

    location = IP2Loc.get_all(ip)
    cache.set("location_ip:%s" % (
            ip
        ),
        location.city,
        timeout=settings.IP2LOCATION_TTL
    )
    return location.city
