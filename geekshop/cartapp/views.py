import json
import os
from django.shortcuts import render
from cartapp.models import Cart
from mainapp.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


path = '..\\geekshop\\mainapp\\templates\\mainapp\\include\\main_menu.json'.replace('\\', os.sep)
with open(path, 'r', encoding='utf-8') as file:
    main_menu = json.load(file)


@login_required 
def cart(request):
    title = 'корзина'
    user_cart = Cart.objects.filter(user=request.user).order_by('product__category')
    return render(request, 'cartapp/cart.html', 
                    context={'title': title,
                            'cart': user_cart,
                            'main_menu': main_menu,}
                    )


@login_required
def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart.objects.filter(user=request.user, product=product).first()
        
    if not cart:
        cart = Cart(user=request.user, product=product)
        
    cart.quantity += 1
    cart.save()
        
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[pk]))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

@login_required
def cart_minus(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart.objects.filter(user=request.user, product=product).first()
    
    if cart is not None:
        if cart.quantity > 0:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_record = Cart.objects.filter(user=request.user, product=product).first()
    cart_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    #return render(request, 'cartapp/cart.html', content)
