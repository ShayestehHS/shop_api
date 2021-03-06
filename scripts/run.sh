#!/bin/sh

set -e

ls -la /vol/
ls -la /vol/web

whoami

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate

cd src
celery -A shop_api worker -l info
cd ..

uwsgi --socket :9000 --workers 4 --master --enable-threads --module shop_api.wsgi