from django.urls import path
from .views import *
from . import views
from django.views.decorators.cache import cache_page

urlpatterns=[
    path('add_category/',AddCategory.as_view(),name='add_category'),
    path('add_brand/',AddBrand.as_view(),name='add_brand'),
    path('add_products/', views.add_product, name='add_products'),
    path('ajax/load-brands/', views.load_brand, name='ajax_load_brands'),
    path('user_management/',User_Management.as_view(), name='user_management'),
    path('user_block/<int:id>/',views.user_block,name='user_block'),
    path('user_unblock/<int:id>/',views.user_unblock,name='user_unblock'),
    path('view_products/',ViewProducts.as_view(),name='view_products'),
    path('edit_products/<slug:slug>/',views.edit_products,name='edit_products'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
    path('delete_products/<int:id>/',views.delete_products,name='delete_products'),
   
    
   
    


]
