from django.contrib.auth.models import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.CharField(max_length=200, help_text="Maximum length is 200.")
    image = models.ImageField(default='image/avatar/default.jpg')
    age = models.IntegerField()
