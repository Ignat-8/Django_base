# Generated by Django 4.0 on 2022-01-12 18:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_shopuser_activation_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 18, 40, 56, 613587, tzinfo=utc)),
        ),
    ]
