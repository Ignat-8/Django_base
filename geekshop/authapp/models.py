from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.dispatch import receiver


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


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    GENDER_CHOICES = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
    )
    user = models.OneToOneField(ShopUser, 
                                unique=True, 
                                null=False, 
                                db_index=True,  # для данного поля создается индекс.
                                on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', 
                                max_length=128,
                                blank=True)
    aboutMe = models.TextField(verbose_name='о себе', 
                                max_length=512,
                                blank=True)
    gender = models.CharField(verbose_name='пол', 
                                max_length=1,
                                choices=GENDER_CHOICES, 
                                blank=True)
    
    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)
    
    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
