import requests

from bs4 import BeautifulSoup
from celery import shared_task
from django.core.cache import cache


@shared_task
def get_gold_carat_24_price():
    url = "https://www.tgju.org/profile/geram24"  # Note: Illegal method
    result = requests.get(url)
    contents = BeautifulSoup(result.text, "html.parser")
    price = contents.find("span", {'data-col': 'info.last_trade.PDrCotVal'}).text
    return cache.set('gold_carat_24', price, timeout=10)


@shared_task
def get_gold_carat_18_price():
    url = "https://www.tgju.org/profile/geram18"  # Note: Illegal method
    result = requests.get(url)
    contents = BeautifulSoup(result.text, "html.parser")
    price = contents.find("span", {'data-col': 'info.last_trade.PDrCotVal'}).text
    return cache.set('gold_carat_18', price, timeout=10)


@shared_task
def get_gold_mesghal_price():
    url = "https://www.tgju.org/profile/mesghal"  # Note: Illegal method
    result = requests.get(url)
    contents = BeautifulSoup(result.text, "html.parser")
    price = contents.find("span", {'data-col': 'info.last_trade.PDrCotVal'}).text
    return cache.set('gold_mesghal', price, timeout=10)
