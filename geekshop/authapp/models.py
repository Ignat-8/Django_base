from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


def default_key_expiration_date():
    return now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name = 'возраст', null=True, default=18)
    city = models.CharField(max_length=64, verbose_name='город')
    phone_number = models.CharField(max_length=12, verbose_name='телефон', blank=True)
    nick_name = models.CharField(max_length=10, blank=False, null=False)
    activation_key = models.CharField(verbose_name = 'ключ активации', max_length=128, blank=True)
    activation_key_expires = models.DateTimeField( default=default_key_expiration_date )

    def is_activation_key_expired(self):
        if now() <= self.activation_key_expires:
            return False
        else:
            return True
