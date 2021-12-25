from django.urls import path
import cartapp.views as cartapp

app_name = 'cartapp'

urlpatterns = [
    path('', cartapp.cart, name='view'),
    path('add/<int:pk>/', cartapp.cart_add, name='add'),
    path('remove/<int:pk>)/', cartapp.cart_remove, name='remove'),
]