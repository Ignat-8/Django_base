from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse
from cartapp.models import Cart
from mainapp.models import Product
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm



class OrderList(ListView):
        model = Order
        def get_queryset(self):
                return Order.objects.filter(user=self.request.user)


class OrderItemsCreate(CreateView):
        model = Order
        fields = []
        success_url = reverse_lazy('ordersapp:orders_list')

        def get_context_data(self, **kwargs):
                data = super(OrderItemsCreate, self).get_context_data(**kwargs)
                OrderFormSet = inlineformset_factory(Order, 
                                                OrderItem,
                                                form=OrderItemForm, 
                                                extra=1)

                if self.request.POST:
                        formset = OrderFormSet(self.request.POST)
                else:
                        cart_items = Cart.get_items(self.request.user)
                        if len(cart_items):
                                OrderFormSet = inlineformset_factory(Order, 
                                                                OrderItem,
                                                                form=OrderItemForm, 
                                                                extra=len(cart_items))
                                formset = OrderFormSet()
                                for num, form in enumerate(formset.forms):
                                        form.initial['product'] = cart_items[num].product
                                        form.initial['quantity'] = cart_items[num].quantity
                                        form.initial['storage'] = cart_items[num].product.quantity
                                        form.initial['price'] = f'{cart_items[num].product.price} руб.'
                        else:
                                formset = OrderFormSet()
                data['orderitems'] = formset
                return data

        def form_valid(self, form):
                context = self.get_context_data()
                orderitems = context['orderitems']
                with transaction.atomic():
                        form.instance.user = self.request.user
                        self.object = form.save()
                        if orderitems.is_valid():
                                orderitems.instance = self.object
                                orderitems.save()
                                # удаляем корзину только в случае сохранения заказа!!!
                                cart_items = Cart.get_items(self.request.user)
                                cart_items.delete() 

                # удаляем пустой заказ
                if self.object.get_total_cost() == 0:
                        self.object.delete()
                return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
        model = Order
        fields = []
        success_url = reverse_lazy('ordersapp:orders_list')

        def get_context_data(self, **kwargs):
                data = super(OrderItemsUpdate, self).get_context_data(**kwargs)
                OrderFormSet = inlineformset_factory(Order, 
                                                OrderItem,
                                                form=OrderItemForm, 
                                                extra=1)
                if self.request.POST:
                        data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
                else:
                        formset = OrderFormSet(instance=self.object)
                        for form in formset.forms:
                                if form.instance.pk:  # новый объект или уже существующий
                                        form.initial['storage'] = form.instance.product.quantity
                                        form.initial['price'] = f'{form.instance.product.price} руб.'
                                        if form.initial['quantity'] > form.initial['storage']:
                                                form.initial['comments']='ошибка - кол-ва на складе'
                                        if form.initial['quantity'] == 0:
                                                form.initial['comments']='ошибка - кол-во = 0'
                        data['orderitems'] = formset
                return data

        def form_valid(self, form):
                context = self.get_context_data()
                # context = {'object': <Order: Текущий заказ: 10>, 
                #            'order': <Order: Текущий заказ: 10>, 
                #            'form': <OrderForm bound=True, valid=Unknown, fields=()>, 
                #            'view': <ordersapp.views.OrderItemsUpdate object at 0x0000018F5E9DB4C0>, 
                #            'orderitems': <django.forms.formsets.OrderItemFormFormSet object at 0x0000018F5EAAABC0>}
                orderitems = context['orderitems']
                # orderitems.forms = [<OrderItemForm bound=True, valid=Unknown, 
                #                       fields=(order;product;quantity;storage;comments;id;DELETE)>, 
                #                     <OrderItemForm bound=True, valid=Unknown, 
                #                       fields=(order;product;quantity;storage;comments;id;DELETE)>]
                with transaction.atomic():
                        self.object = form.save()
                        if orderitems.is_valid():
                                orderitems.instance = self.object
                                orderitems.save()
                c = 0
                for el in orderitems.forms:
                        if int(el['quantity'].value()) == 0 and el['product'].value() != '':
                                c = 1
                        if int(el['quantity'].value())>0 and el['storage'].value() != '':
                                if int(el['quantity'].value()) > int(el['storage'].value()):
                                        c = 1
                # если указано нулевое число или больше чем есть на складе перезагружаем страницу
                if c == 1:  # и даем пользователю исправить значения
                        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
                # удаляем пустой заказ
                if self.object.get_total_cost() == 0:
                        self.object.delete()
                return super(OrderItemsUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
        model = Order
        success_url = reverse_lazy('ordersapp:orders_list')


class OrderRead(DetailView):
        model = Order
        def get_context_data(self, **kwargs):
                context = super(OrderRead, self).get_context_data(**kwargs)
                context['title'] = 'заказ/просмотр'
                return context


def order_forming_complete(request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.SENT_TO_PROCEED
        if not order.reserve_product():  # резервируем товар на складе, т.е. в БД
                return HttpResponseRedirect(reverse('ordersapp:order_error', args=[pk]))
        order.save()
        
        verify_link = reverse('order:orders_list')
        title = f'Заказ пользователя {request.user.username}'
        message = (f"Вы совершили заказ № {order.pk} на портале {settings.DOMAIN_NAME}.\n" + 
                f"Общая сумма заказа {order.get_total_cost()}.\n"
                f"Для просмотра заказа перейдите по ссылке:\n" + 
                f"{settings.DOMAIN_NAME}{verify_link}")

        send_mail(title, message, settings.EMAIL_HOST_USER, [request.user.email], fail_silently=False)
        return HttpResponseRedirect(reverse('ordersapp:orders_list'))


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_product_info(request, pk):
        if is_ajax(request=request):
                products = Product.objects.filter(id=pk)
                data = {'price': products[0].price,
                        'storage': products[0].quantity,
                        'is_active': products[0].is_active}
                return JsonResponse(data)
