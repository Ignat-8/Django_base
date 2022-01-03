from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from mainapp.models import Product, ProductCategory
from adminapp.forms import ProductEditForm


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    else:
        return True


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукт'
    category = get_object_or_404(ProductCategory, pk=pk)
    if pk==1:
        products_list = Product.objects.all().order_by('name')
    else:
        products_list = Product.objects.filter(category__pk=pk).order_by('name')
    
    content = {
        'title': title,
        'category': category,
        'objects': products_list,
        }
    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'продукт/создание'
    
    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm()

    content = {'title': title, 'update_form': product_form, 'pk': pk}
    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/описание'
    product = get_object_or_404(Product, pk=pk)
    content = {'title': title, 'object': product}
    return render(request, 'adminapp/product_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'продукт/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)
    
    content = {'title': title, 'update_form': edit_form, 'pk': edit_product.category_id}
    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'продукт/удаление'
    del_product = get_object_or_404(Product, pk=pk)
    if del_product.is_active:  #при первом нажатии на "удалить" меняем статус
        del_product.is_active = False
        del_product.save()
    else:  # при повторном нажатии на "удалить" удаляем товар из БД
        del_product.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))