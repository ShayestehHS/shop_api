import os

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

# SSL/TLS Settings
# CORS_REPLACE_HTTPS_REFERER = True
# HOST_SCHEME = "https://"
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_SECONDS = 1000000
# SECURE_FRAME_DENY = True

MAILCHIMP_API_KEY = config('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = config('MAILCHIMP_DATA_CENTER')
MAILCHIMP_PUB_KEY = config('MAILCHIMP_PUB_KEY')

MERCHANT = config('MERCHANT')

# Celery configuration
DJANGO_SETTINGS_MODULE = 'settings.production'
BROKER_URL = f'redis://{os.getenv("HOSTNAME")}:6379'
CELERY_RESULT_BACKEND = f'redis://{os.getenv("HOSTNAME")}:6379'

# Cache configuration
CACHES['default']['LOCATION'] = "redis://redis/1"
