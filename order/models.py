from django.db import models
from django.conf import settings

from product.models import Product

User = settings.AUTH_USER_MODEL


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    tax = models.PositiveSmallIntegerField(default=settings.DEFAULT_TAX_PERCENT)
    benefit = models.PositiveSmallIntegerField(default=settings.DEFAULT_BENEFIT_PERCENT)
    wage = models.PositiveSmallIntegerField(help_text='Maximum valid wage per gram is 2,147,483,647')
    calculated_price = models.DecimalField(max_digits=10, decimal_places=2)  # Read only
    calculated_discount = models.DecimalField(max_digits=10, decimal_places=2)  # Read only


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Read only
    address = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="Maximum valid discount is 99,999,999.99")
