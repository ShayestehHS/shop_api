# celery -A shop_api beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
import os

from celery import Celery
from product.tasks import get_gold_carat_18_price, get_gold_carat_24_price

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_api.settings.local')
app = Celery('shop_api')

app.conf.broker_url = f'redis://{os.getenv("HOSTNAME", "localhost")}:6379/0'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'get price gold carat 18': {
        'task': 'product.tasks.get_gold_carat_18_price',
        'schedule': 1,
    },
    'get price gold carat 24': {
        'task': 'product.tasks.get_gold_carat_24_price',
        'schedule': 1,
    },
}