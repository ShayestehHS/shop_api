import datetime
import os
import time

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, BaseValidator
from django.db import models

from ckeditor.fields import RichTextField
from django.utils.text import slugify

User = settings.AUTH_USER_MODEL


def body_validator(value):
    black_list: list = settings.ARTICLE_BODY_BLACK_LIST
    for word in black_list:
        if word in value:
            raise ValidationError(f"{word} is in our black list.")


def get_file_ext(filename):
    base_name = os.path.basename(filename)
    ext = os.path.splitext(base_name)[-1]
    return ext


def upload_article_image_path(instance, filename):
    ext = get_file_ext(filename)
    if ext.lower() not in settings.ARTICLE_ALLOWED_PNG_EXTENSION:
        raise ValueError("Image extension is not allowed.")

    new_filename = f"{instance.slug}-{instance.id}{ext}"
    return os.path.join("image", "article", instance.title, new_filename)


class Article(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=127, help_text="Maximum length is 127 character.")
    slug = models.SlugField(unique=True, max_length=127, help_text="Maximum length is 127 character.")
    image = models.ImageField(upload_to="upload_article_image_path", help_text=f"Valid extensions are: {' '.join(settings.ARTICLE_ALLOWED_PNG_EXTENSION)}")
    body = RichTextField(validators=[body_validator])
    hits = models.IntegerField(default=1)
    is_published = models.BooleanField(default=False)
    last_update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    rater_counts = models.PositiveSmallIntegerField(default=0, help_text="Maximum valid integer is 2,147,483,647")
    average_rating = models.FloatField(default=2.5, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])
    rate = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)], help_text="Maximum rate is 5 and minimum is 0.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "article"
        verbose_name_plural = "articles"
