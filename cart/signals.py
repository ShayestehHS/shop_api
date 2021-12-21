from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from cart.models import Cart
from product.models import Product
from product.utils import get_products_price, get_sum_price


@receiver(m2m_changed, sender=Cart.products.through)
def products_changed(sender, instance: Cart, action, pk_set: set, **kwargs):
    if 'post_' in action:  # post_remove, post_add, post_clear
        products = Product.objects.filter(cart=instance).only('material', 'carat', 'wage', 'weight', 'stone_price')

        products_price = get_products_price(products)
        sum_price = get_sum_price(products_price)

        instance.sum_prices = sum_price
        instance.save(update_fields=['sum_prices'])
