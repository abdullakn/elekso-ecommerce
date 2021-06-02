from django.urls import path
from .views import *
from . import views


urlpatterns=[
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/',views.remove_cart,name='remove_cart'),
    path('remove_cart_item/<int:product_id>/',views.remove_cart_item,name='remove_cart_item'),
    path('checkout/',views.checkout,name='checkout'),
    path('add_cart_ajax/',views.add_cart_ajax,name='add_cart_ajax'),
    path('remove_cart_ajax/',views.remove_cart_ajax,name='remove_cart_ajax')
]