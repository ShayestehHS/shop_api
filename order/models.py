from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.conf import settings

from product.models import Product

User = settings.AUTH_USER_MODEL


class Coupon(models.Model):
    discount_percent = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    discount_amount = models.PositiveSmallIntegerField(default=0)
    code = models.CharField(max_length=15, help_text="Maximum length for code is 15 character.")
    is_valid = models.BooleanField(default=False)
    detail = models.CharField(max_length=255, help_text="Maximum length for detail is 255 character.")

    def __str__(self):
        return self.detail[:10]

    def clean(self):
        if self.discount_amount != 0 and self.discount_percent != 0:
            raise ValidationError("Percent and amount discount can't have value at the same time.")
        elif self.discount_amount == 0 and self.discount_percent == 0:
            raise ValidationError("Percent or amount discount should have value.")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, null=True, blank=True)
    coupon = models.OneToOneField(Coupon, on_delete=models.CASCADE, null=True, blank=True)
    payable_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Read only
    address = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    authority = models.CharField(null=True, blank=True, max_length=36)
    discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text="Maximum valid discount is 99,999,999.99")
