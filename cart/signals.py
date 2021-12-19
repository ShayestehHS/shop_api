from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from cart.models import Cart


@receiver(m2m_changed, sender=Cart.products.through)
def toppings_changed(sender, instance, **kwargs):
    print("changed")
