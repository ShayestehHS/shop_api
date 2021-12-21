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


def get_products_price(products):
    """
        For getting product price we need:
        'material', 'carat', 'wage', 'weight', 'stone_price'
    """
    result = []
    for product in products:
        # material_price = get_material_price_from_cache(product.material,product.carat)
        material_price = 200  # ToDo: Clean this line
        price = (material_price + product.wage) * product.weight * benefit * tax
        price += product.stone_price
        result.append(price)
    return result


def get_sum_price(products_price):
    sum_price = 0
    for price in products_price:
        sum_price += price
    return sum_price
