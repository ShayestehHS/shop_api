import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings.local')
app = Celery('shop_api')

app.conf.broker_url = f'redis://{os.getenv("HOSTNAME","localhost")}:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
