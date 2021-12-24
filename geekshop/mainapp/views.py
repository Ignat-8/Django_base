import json
import os
import random
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import ProductCategory, Product


path = '..\\geekshop\\mainapp\\templates\\mainapp\\include\\main_menu.json'.replace('\\', os.sep)
with open(path, 'r', encoding='utf-8') as file:
    main_menu = json.load(file)


def main(request):
    title = 'главная'
    ProductCategories = ProductCategory.objects.all()
    products = Product.objects.all()
    pk1 = random.randint(1, len(ProductCategories))
    pk2 = random.randint(1, len(ProductCategories))
    return render(request, 'mainapp/index.html', 
                    context={'main_menu': main_menu, 
                            'title': title,
                            'ProductCategories': ProductCategories,
                            'products1': products[pk1],
                            'products2': products[pk2],
                            'pk1':pk1,
                            'pk2':pk2
                            })


def products(request, pk=None):
    title = 'продукты'
    if pk is not None:
        if pk==1:
            category = 'все'
            products = Product.objects.all().order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        return render(request, 'mainapp/products_list.html',
                        context={'main_menu': main_menu,
                                'title': title,
                                'category': category,
                                'products': products,
                                'pk': pk
                                })

    ProductCategories = ProductCategory.objects.all()
    products = Product.objects.all()
    return render(request, 'mainapp/products.html',
                        context={'main_menu': main_menu,
                                'title': title,
                                'ProductCategories': ProductCategories,
                                'products': products
                                })



def contact(request):
    title = 'контакты'
    return render(request, 'mainapp/contact.html',
                  context={'main_menu': main_menu,
                            'title': title,
                           'some_list': ['0', '1', '2']
                           })
