import time

import requests

from bs4 import BeautifulSoup
from celery import shared_task
from django.core.cache import cache
from requests import Response


@shared_task
def get_gold_carat_24_price():
    url = "https://www.tgju.org/profile/geram24"
    result = requests.get(url)
    contents = BeautifulSoup(result.text, "html.parser")
    price = contents.find("span", {'data-col': 'info.last_trade.PDrCotVal'}).text
    cache.set('gold_carat_24', price, timeout=1)
    print(cache.get('gold_carat_24'))


@shared_task
def get_gold_carat_18_price():
    url = "https://www.tgju.org/profile/geram18"
    result = requests.get(url)
    contents = BeautifulSoup(result.text, "html.parser")
    price = contents.find("span", {'data-col': 'info.last_trade.PDrCotVal'}).text
    cache.set('gold_carat_18', price, timeout=1)
    print(cache.get('gold_carat_18'))
