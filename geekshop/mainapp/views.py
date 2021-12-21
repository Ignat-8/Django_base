import json
from django.shortcuts import render
from .models import ProductCategory, Product
#from authapp.models import ShopUser


with open('..\\geekshop\\mainapp\\templates\\mainapp\\include\\main_menu.json', 'r', encoding='utf-8') as file:
    main_menu = json.load(file)


def main(request):
    title = 'главная'
    #active_user = request.GET['user']
    return render(request, 'mainapp/index.html', 
                    context={'main_menu': main_menu, 
                            'title': title,
                            #'active_user': active_user
                            })


def products(request, pk=1):
    title = 'продукты'
    products = Product.objects.all()
    ProductCategories = ProductCategory.objects.all()
    #active_user = request.GET['user']
    return render(request, 'mainapp/products.html',
                  context={'main_menu': main_menu,
                            'title': title,
                            'ProductCategories': ProductCategories,
                            'products': products,
                            #'active_user': active_user
                           })


def contact(request):
    title = 'контакты'
    #active_user = request.GET['user']
    return render(request, 'mainapp/contact.html',
                  context={'main_menu': main_menu,
                            'title': title,
                            #'active_user': active_user,
                           'some_list': ['0', '1', '2']
                           })
