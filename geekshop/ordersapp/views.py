from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.forms import inlineformset_factory
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from cartapp.models import Cart
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

                                cart_items.delete()
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

                # удаляем пустой заказ
                if self.object.get_total_cost() == 0:
                        self.object.delete()
                return super(OrderItemsCreate, self).form_valid(form)


class OrderItemsUpdate(UpdateView):
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
                        data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
                else:
                        data['orderitems'] = OrderFormSet(instance=self.object)
                return data

        def form_valid(self, form):
                context = self.get_context_data()
                orderitems = context['orderitems']

                with transaction.atomic():
                        self.object = form.save()
                        if orderitems.is_valid():
                                orderitems.instance = self.object
                                orderitems.save()

                # удаляем пустой заказ
                if self.object.get_total_cost() == 0:
                        self.object.delete()
                return super(OrderItemsCreate, self).form_valid(form)


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
        order.save()
        return HttpResponseRedirect(reverse('ordersapp:orders_list'))




