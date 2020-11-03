#!/bin/sh
cd /code/miniweather
celery -A miniweather beat # --logfile=/storage/logs/celery_beat.log 