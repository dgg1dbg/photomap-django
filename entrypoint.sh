#!/bin/sh
python manage.py makemigrations api
python manage.py migrate

exec gunicorn photomap.wsgi:application --bind 0.0.0.0:8000