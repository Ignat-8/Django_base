import json, os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser

JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name), 'r', encoding="utf-8") as infile:
        return json.load(infile)


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        categories = load_from_json('categories.json')
        ProductCategory.objects.all().delete()
        with connection.cursor() as cursor: # обнуляем AutoIncrement
            cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='mainapp_productcategory'")
        
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()
       
        products = load_from_json('products.json')
        Product.objects.all().delete()
        with connection.cursor() as cursor: # обнуляем AutoIncrement
            cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='mainapp_product'")

        for product in products:
            new_product = Product(**product)
            new_product.save()
        
        # Создаем суперпользователя при помощи менеджера модели
        #super_user = ShopUser.objects.create_superuser(username='user', 
        #                                                email='user@localhost.ru', 
        #                                                nick_name='user',
        #                                                city='localhost',
        #                                                age=0)
