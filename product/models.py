import os

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager

CARAT_CHOICES = [
    ("24", "24 carat"),
    ("18", "18 carat"),
]
COLOR_CHOICES = [
    ('y', 'Yellow'),
    ('w', 'White'),
]
MATERIAL_CHOICES = [
    ('g', 'Gold'),
    ('s', 'Sliver'),
    ('c', 'Copper'),
    ('a', 'Aluminium'),
]


def get_file_ext(value):
    base_name = os.path.basename(value)
    ext = os.path.splitext(base_name)[-1]
    return ext


def ext_validator(filename):
    valid_ext: list = settings.PRODUCT_ALLOWED_PNG_EXTENSION
    ext = get_file_ext(filename.name)

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


class Product(models.Model):
    name = models.CharField(max_length=127, help_text="Maximum length is 127 character.")
    slug = models.SlugField(unique=True, allow_unicode=True, max_length=255, help_text="Maximum length is 255 character.")
    image = models.ImageField(upload_to='upload_product_image_path', validators=[ext_validator])
    body = RichTextField(validators=[body_validator])
    in_store = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    # ToDo: category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    count = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")
    color = models.CharField(default='y', choices=COLOR_CHOICES, max_length=6)
    weight = models.PositiveSmallIntegerField(default=1)
    carat = models.CharField(choices=CARAT_CHOICES, max_length=2)
    average_rate = models.FloatField(default=2.5, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])

    is_have_stone = models.BooleanField(default=False)
    stone_price = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")
    purchase_price = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")
    price = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if self.is_have_stone != self.stone_price:  # True,0 OR False,PositiveInteger
            raise ValidationError("Stone of this product doesn't have any price.")
        if not self.slug:
            self.slug = slugify(self.name)

        self.full_clean()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'product'
        verbose_name_plural = 'products'


class ProductRate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MaxValueValidator(5.00), MinValueValidator(0.00)], help_text="Maximum rate is 5.00 and minimum is 0.00 .")
