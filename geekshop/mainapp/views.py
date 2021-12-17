import json
from django.shortcuts import render
from .models import ProductCategory, Product


with open('..\\geekshop\\mainapp\\templates\\mainapp\\include\\main_menu.json', 'r', encoding='utf-8') as file:
    main_menu = json.load(file)


with open('..\\geekshop\\mainapp\\templates\\mainapp\\include\\products_menu.json', 'r', encoding='utf-8') as file:
    products_menu = json.load(file)


def main(request):
    title = 'главная'
    return render(request, 'mainapp/index.html', 
                    context={'main_menu': main_menu, 
                            'title': title
                            })


def products(request, pk=None):
    print('---------------------------------------------------')
    print('Call category number ', pk)
    print('---------------------------------------------------')
    title = 'продукты'
    products = Product.objects.all()
    ProductCategories = ProductCategory.objects.all()
    return render(request, 'mainapp/products.html',
                  context={'main_menu': main_menu,
                            'title': title,
                            #'products_menu': products_menu,
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
