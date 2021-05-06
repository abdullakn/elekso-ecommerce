from django.urls import path
from .views import *
from . import views

urlpatterns=[
    # path('login/',sample_view,name='sample_view'),
    # path('register',register,name='register'),
    path('registeration/',UserRegistation.as_view(),name='user_registration'),
    path('login/',Login.as_view(),name='login'),
    path('admin_login/',AdminLogin.as_view(),name='admin_login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('',views.user_home,name='user_home'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('product_details/<slug:slug>/',views.product_details,name='product_details'),
    path('check_user/',views.check_user,name='check_user') ,
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('product_store/<int:id>/',views.product_store,name='product_store')
]