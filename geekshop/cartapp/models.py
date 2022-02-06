from django.db import models
from django.conf import settings
from mainapp.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                            on_delete=models.CASCADE,
                            related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    @classmethod
    def get_items(self, user):
        return Cart.objects.filter(user=user)

    @property
    def product_price(self):
        return  '{:,.2f}'.format(self.product.price).replace(',',' ')

    @property
    def product_cost(self):
        "return cost of all products this type"
        prod_cost = self.product.price * self.quantity
        return  '{:,.2f}'.format(prod_cost).replace(',',' ')

    @property 
    def total_quantity(self):
        "return total quantity for user"
        _items = Cart.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity 
    
    @property
    def total_cost(self):
        "return total cost for user"
        _items = Cart.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product.price * x.quantity, _items)))
        return '{:,.2f}'.format(_totalcost).replace(',',' ')
