# Generated by Django 4.0 on 2022-01-29 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordersapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='storage',
            field=models.PositiveIntegerField(default=0, verbose_name='на складе'),
        ),
    ]
