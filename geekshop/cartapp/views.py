from django.shortcuts import render
from cartapp.models import Cart
from mainapp.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


def cart(request):
    return render(request, 'cartapp/cart.html', context={'cart': request.user.cart.all()})


def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart.objects.filter(user=request.user, product=product).first()
    
    if not cart:
        cart = Cart(user=request.user, product=product)
    
    cart.quantity += 1
    cart.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, pk):
    content = {}
    return render(request, 'cartapp/cart.html', content)
