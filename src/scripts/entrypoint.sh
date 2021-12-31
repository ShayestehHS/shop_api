#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations

uwsgi --module shop_api.wsgi --socket :8000 --master --enable-threads