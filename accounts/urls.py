from django.urls import path
from .views import *
from . import views
from .views import user_profile,user_address,collect_address,user_order,cancel_order,user_propic

urlpatterns=[
    # path('login/',sample_view,name='sample_view'),
    # path('register',register,name='register'),
    path('registeration/',UserRegistation.as_view(),name='user_registration'),
    path('login/',Login.as_view(),name='login'),
    path('admin/login/',AdminLogin.as_view(),name='admin_login'),
    path('admin/home/',views.admin_home,name='admin_home'),
    path('',views.user_home,name='user_home'),
    path('user_logout/',views.user_logout,name='user_logout'),
    path('product_details/<slug:slug>/',views.product_details,name='product_details'),
    path('check_user/',views.check_user,name='check_user') ,
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('product_store/<str:slug>/',views.product_store,name='product_store'),
    path('user_accounts/',views.user_accounts,name='user_accounts'),
    path('user_profile/',views.user_profile,name='user_profile'),
    path('user_address/',views.user_address,name='user_address'),
    path('edit_address/<int:id>/',views.edit_address,name='edit_address'),
    path('delete_address/<int:id>/',views.delete_address,name='delete_address'),
    path('collect_address/',views.collect_address,name='collect_address'),
    path('search_product/',views.search_product,name='search_product'),
    path('user_order/',views.user_order,name='user_order'),
    path('cancel_order/<int:id>/',views.cancel_order,name='cancel_order'),
    path('user_propic/',views.user_propic,name='user_propic'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),
    path('login_otp/',views.login_otp,name='login_otp'),
    path('verify_otp/',views.verify_otp,name='verify_otp'),
    path('filter_brand/<str:brand>/',views.filter_brand,name='filter_brand'),
    path('submit_review/<int:id>/',views.submit_review,name='submit_review'),
    path('check_referal/',views.check_referal,name='check_referal'),
    path('verify_coupen/',views.verify_coupen,name='verify_coupen')
    

    # path('filter_product',views.filter_product,name='filter_product')
]