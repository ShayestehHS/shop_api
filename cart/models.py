from django.db import models
from django.conf import settings

from product.models import Product

User = settings.AUTH_USER_MODEL


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    sum_prices = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")

    def __str__(self):
        return f'cart of user:{self.user_id}'
