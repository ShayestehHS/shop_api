from django.db import models
from django.conf import settings

from product.models import Product

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Read only
    address = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="Maximum valid discount is 99,999,999.99")
