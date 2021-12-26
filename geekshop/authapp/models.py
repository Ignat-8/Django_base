from django.db import models
from django.contrib.auth.models import AbstractUser


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'возраст', null=True)
    city = models.CharField(max_length=64, verbose_name='город')
    phone_number = models.CharField(max_length=12, verbose_name='телефон', blank=True)
    nick_name = models.CharField(max_length=10, blank=False, null=False)
