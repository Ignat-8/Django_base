import json
import os
import random
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import ProductCategory, Product
from cartapp.models import Cart


path = '..\\geekshop\\mainapp\\templates\\mainapp\\include\\main_menu.json'.replace('\\', os.sep)
with open(path, 'r', encoding='utf-8') as file:
    main_menu = json.load(file)


def main(request):
    title = 'главная'
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

    ProductCategories = ProductCategory.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    pk1 = random.randint(1, len(ProductCategories))
    pk2 = random.randint(1, len(ProductCategories))
    return render(request, 'mainapp/index.html', 
                    context={'main_menu': main_menu, 
                            'title': title,
                            'ProductCategories': ProductCategories,
                            'products1': products[pk1],
                            'products2': products[pk2],
                            'pk1':pk1,
                            'pk2':pk2,
                            'cart':cart
                            })


def products(request, pk=None):
    title = 'продукты'
    ProductCategories = ProductCategory.objects.filter(is_active=True)
    
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

    if pk is not None:
        if pk==1:
            category = 'все'
            sql = f'''select t1.*, t2.quantity as cart_quantity
                            , case when t2.id is null then 0 else t2.quantity*t1.price end as total_price
                      from mainapp_product t1
                      left join (select cc.*
			                     from cartapp_cart cc
			                     join authapp_shopuser sh on cc.user_id=sh.id
			                     where sh.username='{request.user}') t2 on t2.product_id=t1.id
                        where t1.is_active=True'''
        else:
            category = get_object_or_404(ProductCategory, pk=pk, is_active=True)
            #products = Product.objects.filter(category__pk=pk).order_by('price')
            sql = f'''select t1.*, t2.quantity as cart_quantity
                            , case when t2.id is null then 0 else t2.quantity*t1.price end as total_price
                      from mainapp_product t1
                      left join (select cc.*
			                     from cartapp_cart cc
			                     join authapp_shopuser sh on cc.user_id=sh.id
			                     where sh.username='{request.user}') t2 on t2.product_id=t1.id 
                      where t1.category_id={pk} and t1.is_active=True'''

        products = Product.objects.raw(sql)
        
        for prod in products:  # форматируем стоимость к виду # ###.00
            prod.total_price = '{:,.2f}'.format(prod.total_price).replace(',',' ')

        
        return render(request, 'mainapp/products_list.html',
                        context={'main_menu': main_menu,
                                'title': title,
                                'category': category,
                                'products': products,
                                'ProductCategories': ProductCategories,
                                'pk': pk,
                                'cart': cart,
                                })

    products = Product.objects.filter(is_active=True)
    hot_product = random.sample(list(products), 1)[0]
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]

    return render(request, 'mainapp/products.html',
                        context={'main_menu': main_menu,
                                'title': title,
                                'ProductCategories': ProductCategories,
                                'cart':cart,
                                'hot_product': hot_product,
                                'same_products': same_products
                                })


def contact(request):
    title = 'контакты'
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

    return render(request, 'mainapp/contact.html',
                  context={'main_menu': main_menu,
                            'title': title,
                            'cart':cart,
                           'some_list': ['0', '1', '2']
                           })


def product(request, pk):
    title = 'продукты'
    ProductCategories = ProductCategory.objects.filter(is_active=True)
    product = get_object_or_404(Product, pk=pk)
    cart = []
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)

    return render(request, 'mainapp/product.html', 
                    context = {'title': title,
                                'main_menu': main_menu,
                                'product': product,
                                'cart':cart,
                                'ProductCategories': ProductCategories,
                        })