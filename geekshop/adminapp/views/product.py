from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from mainapp.models import Product, ProductCategory


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    else:
        return True


class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 2
    # self.kwargs['pk'] - здесь это номер категории, из которой выводятся продукты

    def get_queryset(self):
        if self.kwargs['pk'] != 1:
            return Product.objects.filter(category=self.kwargs['pk'])
        else:
            return Product.objects.all()
    
    def get_category_name(self):
        return list(ProductCategory.objects.filter(id=self.kwargs['pk']))[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукты/категории'
        context['category_id'] = self.kwargs['pk']
        context['category_name'] = self.get_category_name()
        return context
    
    @method_decorator(user_passes_test(check_is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'
    # self.kwargs['pk'] - здесь это номер обновляемого продукта 

    def get_category_id(self):
        return list(Product.objects.filter(id=self.kwargs['pk']))[0].category_id

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.get_category_id(), 1])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'товары/редактирование'
        context['page'] = self.request.META.get('HTTP_REFERER').split("/")[-2]
        context['category_id'] = self.get_category_id()
        return context


class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'
    # self.kwargs['pk'] - здесь это номер категории, в которой создается продукт 

    def get_initial(self):
        return {'category': self.kwargs['pk']}

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.kwargs['pk'], 1])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'товары/создание'
        context['page'] = self.request.META.get('HTTP_REFERER').split("/")[-2]
        context['category_id'] = self.kwargs['pk']
        return context


class ProductDetailView(DetailView):
    # self.kwargs['pk'] - здесь это номер просматриваемого продукта 
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_category_id(self):
        return list(Product.objects.filter(id=self.kwargs['pk']))[0].category_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'товары/подробнее'
        context['page'] = self.request.META.get('HTTP_REFERER').split("/")[-2]
        context['category_id'] = self.get_category_id()
        return context


class ProductDeleteView(DeleteView):
    # self.kwargs['pk'] - здесь это номер удаляемого продукта 
    model = Product
    #template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        return context

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_active:
            self.object.is_active = False
            self.object.save()
        elif self.get_cnt_product() == 0:
            self.object.delete()
        return HttpResponseRedirect(self.get_success_url())
