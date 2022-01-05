from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from mainapp.models import ProductCategory, Product


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    else:
        return True


class ProductCategoryListView(ListView):
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


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')
    
    def get_cnt_product(self):
        # количество продуктов в удаляемой категории
        sql = f'''select id, count(*) as cnt_products
                  from mainapp_product  
                  where category_id={self.object.id}'''
        return Product.objects.raw(sql)[0].cnt_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/удаление'
        context['cnt_products'] = self.get_cnt_product()
        return context

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
        elif self.get_cnt_product() == 0:
            self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
