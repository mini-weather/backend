# Pull base image
FROM python:3.9-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y g++ gcc gettext gdal-bin nginx
RUN export LC_ALL=C
RUN mkdir -p /usr/share/nginx/html/
RUN rm -rf /usr/share/nginx/html/*
RUN rm -rf /etc/nginx/sites-enabled/*
RUN pip install uwsgi
# Set work directory
WORKDIR /code
# Install dependencies
COPY requirements.pip /code/requirements.pip
RUN pip install -r requirements.pip
RUN pip install 'requests[socks]'
COPY nginx.conf /etc/nginx/conf.d/
COPY *.sh /code/

# Copy project
COPY miniweather /code/miniweather
