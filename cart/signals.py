from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from cart.models import Cart
from product.models import Product


@receiver(m2m_changed, sender=Cart.products.through)
def products_changed(sender, instance: Cart, action, pk_set: set, **kwargs):
    if 'post_' in action:  # post_remove, post_add, post_clear
        products = Product.objects.filter(cart=instance).only('price')
        sum_price = 0
        for product in products:
            sum_price += product.price

        instance.sum_prices = sum_price
        instance.save(update_fields=['sum_prices'])
