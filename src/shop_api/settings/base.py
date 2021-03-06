"""
Django settings for shop_api project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os.path
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "CHANGE-ME"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 0

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]
THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'ckeditor',
    'taggit',
    'taggit_serializer',
    'django_celery_beat',
    'django_comments_xtd',
    'django_comments',
]
LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'article.apps.ArticleConfig',
    'product.apps.ProductConfig',
    'order.apps.OrderConfig',
    'cart.apps.CartConfig',
]
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop_api.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

MINIMUM_LENGTH_PASSWORD = 9
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': MINIMUM_LENGTH_PASSWORD,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "accounts.User"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Site configuration
TAX_PERCENT = 9
BENEFIT_PERCENT = 7
DEFAULT_PAGINATION = 5
DEFAULT_MAX_PAGINATION = 15
DEFAULT_ALLOWED_PNG_EXTENSION = ['.png', '.jpg']
DEFAULT_BODY_BLACK_LIST = ['bad word', 'ugly', 'laravel', 'php']

# Zarrinpal configuration
MERCHANT = "CHANGE-ME"
DEFAULT_ZP_DESCRIPTION = "Thank you"
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_START_PAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

# Article configuration
ARTICLE_PAGINATION = DEFAULT_PAGINATION
ARTICLE_MAX_PAGINATION = DEFAULT_MAX_PAGINATION
ARTICLE_ALLOWED_PNG_EXTENSION = DEFAULT_ALLOWED_PNG_EXTENSION
ARTICLE_BODY_BLACK_LIST = DEFAULT_BODY_BLACK_LIST

# Order configuration
ORDER_PAGINATION = DEFAULT_PAGINATION
ORDER_MAX_PAGINATION = DEFAULT_MAX_PAGINATION

# Product configuration
PRODUCT_PAGINATION = DEFAULT_PAGINATION
PRODUCT_MAX_PAGINATION = DEFAULT_MAX_PAGINATION
PRODUCT_ALLOWED_PNG_EXTENSION = DEFAULT_ALLOWED_PNG_EXTENSION
PRODUCT_BODY_BLACK_LIST = DEFAULT_BODY_BLACK_LIST

# DRF configuration
SITE_ID = 1
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'access'
JWT_AUTH_REFRESH_COOKIE = 'refresh'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# Django-Rest-Auth configuration
REST_AUTH_SERIALIZERS = {
    'LOGIN_SERIALIZER': 'accounts.api.serializers.CustomLoginSerializer',
}

# JWT configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # Create new refresh token and send it to user
    'BLACKLIST_AFTER_ROTATION': True,  # Expire last refresh token after creating new one
    'UPDATE_LAST_LOGIN': True,
}
LOGOUT_ON_PASSWORD_CHANGE = True

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = "CHANGE-ME"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = "CHANGE-ME"
EMAIL_HOST = "CHANGE-ME"
EMAIL_PORT = 465
EMAIL_USE_SSL = True

# django-comment-xtd config
COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_API_GET_USER_AVATAR = "shop_api.utils.get_avatar_url"
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_MAX_THREAD_LEVEL_BY_APP_MODEL = {
    'article.article': 5,
    'product.product': 5,
}

# Celery configuration
DJANGO_SETTINGS_MODULE = 'settings.base'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 min

# Cache configuration
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        'TIMEOUT': 600,  # 10 minutes
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
