from decouple import config

from shop_api.settings.base import *

DEBUG = config("DEBUG", default=0)
# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS.extend(filter(None, config("DJANGO_ALLOWED_HOSTS", default="*").split(" ")))
SECRET_KEY = config('SECRET_KEY')

DOMAIN_NAME = 'shayestehhs.ir'

STATIC_URL = '/static/static/'
MEDIA_URL = '/static/media/'

STATIC_ROOT = '/vol/web/static'
MEDIA_ROOT = '/vol/web/media'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'PORT': '5432',
    }
}

# Celery configuration
DJANGO_SETTINGS_MODULE = 'settings.production'
BROKER_URL = f'redis://{config("REDIS_HOST")}:6379'
CELERY_RESULT_BACKEND = f'redis://{config("REDIS_HOST")}:6379'

# Cache configuration
CACHES['default']['LOCATION'] = "redis://redis/1"

# Email config
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_SSL = config('EMAIL_USE_SSL')
