from django.conf import settings
from django.core.cache import cache

TAX_PERCENT = getattr(settings, 'TAX_PERCENT', 9)
BENEFIT_PERCENT = getattr(settings, 'BENEFIT_PERCENT', 7)

benefit = (100 + BENEFIT_PERCENT) / 100
tax = (100 + TAX_PERCENT) / 100


def validate_carat(carat: str):
    try:
        int(carat)
    except ValueError:
        if '24' not in carat or '18' not in carat:
            carat = 24 if '24' in carat else 18
        else:
            int(carat)  # Raise ValueError
    return carat  # Return valid carat


def get_gold_price_from_cache(carat: str):
    carat: str = validate_carat(carat)  # '24' or '18'
    price: str = cache.get(f'gold_carat_{carat}')
    price: str = price.replace(',', '')
    price: int = int(price)
    return price


def get_price(product):
    material_price = 2  # ToDo: Clean this line
    price = (material_price + product.wage) * product.weight * benefit * tax
    price += product.stone_price
    return price


def get_products_price(products):
    """
        For getting products price we need:
        'id', 'carat', 'wage', 'weight', 'stone_price'
    """
    result = []
    for product in products:
        price = cache.get(f'products:{product.id}:price')
        if price is None:
            price = get_price(product)
            cache.set(f'products:{product.id}:price', price, timeout=30)
            result.append(price)

    return result


def get_sum_price(products_price):
    sum_price = 0
    for price in products_price:
        sum_price += price
    return sum_price
