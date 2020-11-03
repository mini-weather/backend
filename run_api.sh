#!/bin/bash
mkdir /static
cd /code/miniweather
./manage.py migrate
./manage.py collectstatic --noinput
./manage.py compilemessages
service nginx start
if [ "$1" == "release" ]; then
    uwsgi --http :8100 --chdir /code/miniweather --wsgi-file /code/miniweather/miniweather/wsgi.py --master
else
    ./manage.py runserver 0.0.0.0:8100
fi