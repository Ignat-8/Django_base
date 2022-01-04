from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from mainapp.models import ProductCategory
from adminapp.forms import ProductCategoryEditForm


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    else:
        return True


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'
    
    @method_decorator(user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

        
class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


#@user_passes_test(check_is_superuser)
#def categories(request):
#    title = 'админка/категории'
#    categories_list = ProductCategory.objects.all()
#    content = {
#        'title': title,
#        'objects': categories_list
#        }
#    return render(request, 'adminapp/categories.html', content)


#@user_passes_test(check_is_superuser)
#def category_create(request):
#    title = 'категории/создание'
#    
#    if request.method == 'POST':
#        category_form = ProductCategoryEditForm(request.POST, request.FILES)
#        if category_form.is_valid():
#            category_form.save()
#            return HttpResponseRedirect(reverse('admin:categories'))
#    else:
#        category_form = ProductCategoryEditForm()
#    
#    content = {'title': title, 'update_form': category_form}
#    return render(request, 'adminapp/category_update.html', content)


#@user_passes_test(check_is_superuser)
#def category_update(request, pk):
#    title = 'категории/редактирование'
#    edit_category = get_object_or_404(ProductCategory, pk=pk)
#    
#    if request.method == 'POST':
#        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)
#        if edit_form.is_valid():
#            edit_form.save()
#            return HttpResponseRedirect(reverse('admin:category_update', args=[edit_category.pk]))
#    else:
#        edit_form = ProductCategoryEditForm(instance=edit_category)
#    
#    content = {'title': title, 'update_form': edit_form}
#    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(check_is_superuser)
def category_delete(request, pk):
    title = 'категории/удаление'
    del_category = get_object_or_404(ProductCategory, pk=pk)
    del_category.is_active = False
    del_category.save()
    return HttpResponseRedirect(reverse('admin:categories'))