#!/bin/sh
cd /code/miniweather
celery -A miniweather worker -Q now_playing