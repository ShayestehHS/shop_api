from order.models import Order
from product.models import Product


def update_products_count(order: Order):
    products = Product.objects.filter(order=order)
    for product in products:
        product.count -= 1
        if product.count < 1: product.in_store = False

    Product.objects.bulk_update(products, ['count', 'in_store'])
