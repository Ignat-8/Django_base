from django.shortcuts import render
import json

# Create your views here.

with open('..\\geekshop\\mainapp\\templates\\mainapp\\include\\main_menu.json', 'r', encoding='utf-8') as file:
    main_menu = json.load(file)


with open('..\\geekshop\\mainapp\\templates\\mainapp\\include\\products_menu.json', 'r', encoding='utf-8') as file:
    products_menu = json.load(file)


def main(request):
    return render(request, 'mainapp/index.html', context={'main_menu': main_menu})


def products(request):
    return render(request, 'mainapp/products.html',
                  context={'main_menu': main_menu,
                           'products_menu': products_menu
                           })


def contact(request):
    return render(request, 'mainapp/contact.html',
                  context={'main_menu': main_menu,
                           'some_list': ['0', '1', '2']
                           })
