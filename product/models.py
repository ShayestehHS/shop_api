import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

CHOICES_CARAT = [
    ("24", "24 carat"),
    ("22", "22 carat"),
    ("18", "18 carat"),
    ("14", "14 carat"),
    ("8", "8 carat"),
]
CHOICES_STATUS = [
    ('r', 'returned'),
    ('p', 'published'),
    ('d', 'drafted'),
]


def get_file_ext(value):
    base_name = os.path.basename(value)
    ext = os.path.splitext(base_name)[-1]
    return ext


def ext_validator(filename):
    valid_ext: list = settings.PRODUCT_ALLOWED_PNG_EXTENSION
    ext = get_file_ext(filename.url)

    if ext not in valid_ext:
        raise ValidationError(f"{ext} is not in our valid extension list.")


def body_validator(value):
    black_list: list = settings.PRODUCT_BODY_BLACK_LIST
    for word in black_list:
        if word in value:
            raise ValidationError(f"{word} is in our black list.")


def upload_product_image_path(instance, filename):
    ext = get_file_ext(filename)
    new_filename = f"{instance.slug}-{instance.id}{ext}"
    return os.path.join("image", "product", instance.name, new_filename)


class Size(models.Model):
    size = models.PositiveSmallIntegerField()


class Color(models.Model):
    color = models.CharField(unique=True, max_length=15, help_text="Maximum length for color is 15 character.")


class Product(models.Model):
    name = models.CharField(max_length=127, help_text="Maximum length is 127 character.")
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=255, help_text="Maximum length is 255 character.")
    image = models.ImageField(upload_to='upload_product_image_path', validators=[ext_validator])
    body = RichTextField(validators=[body_validator])
    iframe = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=CHOICES_STATUS)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    # ToDo: category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    count = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")
    color = models.ManyToManyField(Color)
    size = models.ManyToManyField(Size)
    carat = models.CharField(choices=CHOICES_CARAT, max_length=2)
    weight = models.DecimalField(max_digits=6, decimal_places=3, help_text="Maximum weight is 999.999.")
    length = models.DecimalField(max_digits=5, decimal_places=3, help_text="Maximum weight is 99.999.", null=True, blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=3, help_text="Maximum weight is 99.999.", null=True, blank=True)

    is_jewelery = models.BooleanField(default=False)
    is_gold = models.BooleanField(default=True)

    # If product is gold
    is_rate_fixed = models.BooleanField(default=False)
    provider_gold_rate = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, help_text="Maximum rate is 99999.999.")

    # If product is jewelry
    provider_diamond_price = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, help_text="Maximum rate is 99999.999.")

    rater_counts = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")
    average_rating = models.FloatField(default=2.5, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)], help_text="Maximum rate is 5 and minimum is 0.")

    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if self.is_gold != self.is_jewelery:
            raise ValidationError("Product can't be gold or jewelery at the same time.")

        self.full_clean()
        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'product'
        verbose_name_plural = 'products'
