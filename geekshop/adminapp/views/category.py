from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from mainapp.models import ProductCategory
from adminapp.forms import ProductCategoryEditForm


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    else:
        return True

        
@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'
    categories_list = ProductCategory.objects.all()
    content = {
        'title': title,
        'objects': categories_list
        }
    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории/создание'
    
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()
    
    content = {'title': title, 'update_form': category_form}
    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категории/редактирование'
    edit_category = get_object_or_404(ProductCategory, pk=pk)
    
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)
    
    content = {'title': title, 'update_form': edit_form}
    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категории/удаление'
    del_category = get_object_or_404(ProductCategory, pk=pk)
    del_category.is_active = False
    del_category.save()
    return HttpResponseRedirect(reverse('admin:categories'))