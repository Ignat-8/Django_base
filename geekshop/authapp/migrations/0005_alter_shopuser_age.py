# Generated by Django 4.0 on 2022-01-16 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_alter_shopuser_activation_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='age',
            field=models.PositiveIntegerField(default=18, null=True, verbose_name='возраст'),
        ),
    ]
