from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from mainapp.models import Product, ProductCategory
from cartapp.models import Cart


def check_is_superuser(user):
    if not user.is_superuser:
        raise PermissionDenied
    else:
        return True


class ProductListView(ListView):
    # self.kwargs['pk'] - здесь это номер категории, из которой выводятся продукты
    model = Product
    template_name = 'adminapp/products.html'
    paginate_by = 3

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
    # self.kwargs['pk'] - здесь это номер обновляемого продукта
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__'

    def get_category_id(self):
        return list(Product.objects.filter(id=self.kwargs['pk']))[0].category_id

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.get_category_id(), 1])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/редактирование'
        context['page'] = self.request.META.get('HTTP_REFERER').split("/")[-2]
        context['category_id'] = self.get_category_id()
        return context


class ProductCreateView(CreateView):
    # self.kwargs['pk'] - здесь это номер категории, в которой создается продукт
    model = Product
    template_name = 'adminapp/product_update.html'
    fields = '__all__' 

    def get_initial(self):
        return {'category': self.kwargs['pk']}

    def get_success_url(self):
        return reverse_lazy('admin:products', args=[self.kwargs['pk'], 1])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/создание'
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
        context['title'] = 'продукт/подробнее'
        context['page'] = self.request.META.get('HTTP_REFERER').split("/")[-2]
        context['category_id'] = self.get_category_id()
        return context


class ProductDeleteView(DeleteView):
    # self.kwargs['pk'] - здесь это номер удаляемого продукта 
    model = Product
    template_name = 'adminapp/product_delete.html'

    def check_product_in_cart(self):
        # проверяем есть ли удаляемый продукт в корзине пользователей
        sql = f'''select cc.id 
                  from cartapp_cart cc 
                  where cc.product_id={self.kwargs['pk']}'''
        if list(Cart.objects.raw(sql)) == []:
            return False
        else:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'продукт/удаление'
        context['page'] = self.request.META.get('HTTP_REFERER').split("/")[-2]
        context['category_id'] = self.get_category_id()
        context['check_product_in_cart'] = self.check_product_in_cart()
        return context

    def get_category_id(self):
        return list(Product.objects.filter(id=self.kwargs['pk']))[0].category_id
        
    def get_success_url(self):
        return reverse('admin:products', args=[self.kwargs['category_id'], 1])

    def form_valid(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.kwargs['category_id'] = self.get_category_id()
        if self.object.is_active:  # при первом нажатии на "удалить" меняем статус
            self.object.is_active = False
            self.object.save()
        elif self.check_product_in_cart() == False:  # при повторном нажатии на "удалить" удаляем из БД
            self.object.delete()  # если данного продукта нет ни в одной из корзин пользователей
        return HttpResponseRedirect(self.get_success_url())
