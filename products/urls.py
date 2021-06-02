from django.urls import path
from .views import *
from . import views
from .views import edit_order_status,view_detailed_order
from django.views.decorators.cache import cache_page

urlpatterns=[
    path('add_category/',views.add_category,name='add_category'),
    path('add_brand/',views.add_brand,name='add_brand'),
    path('edit_category/<int:id>/',views.edit_category,name='edit_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),
    path('view_category/',views.view_category,name='view_category'),
    path('add_products/', views.add_product, name='add_products'),
    path('ajax/load-brands/', views.load_brand, name='ajax_load_brands'),
    path('user_management/',views.user_management, name='user_management'),
    path('user_block/<int:id>/',views.user_block,name='user_block'),
    path('user_unblock/<int:id>/',views.user_unblock,name='user_unblock'),
    path('view_products/',views.view_products,name='view_products'),
    path('edit_products/<slug:slug>/',views.edit_products,name='edit_products'),
    path('delete_user/<int:id>/',views.delete_user,name='delete_user'),
    path('delete_products/<int:id>/',views.delete_products,name='delete_products'),
    path('view_order/',views.view_order,name='view_order'),
    path('edit_order_status/<int:id>/',views.edit_order_status,name='edit_order_status'),
    path('view_detailed_order/<int:id>/',views.view_detailed_order,name='view_detailed_order'),
    path('monthly_report/',views.monthly_report,name='monthly_report'),
    path('yearly_report/',views.yearly_report,name='yearly_report'),
    path('datewise_report/',views.datewise_report,name='datewise_report'),
    path('add_offer/',views.add_offer,name='add_offer'),
    path('category_offer',views.category_offer,name='category_offer'),
    path('product_offer/',views.product_offer,name='product_offer'),
    path('view_offer/',views.view_offer,name='view_offer'),
    path('delete_cat_offer/<int:id>/',views.delete_cat_offer,name='delete_cat_offer'),
    path('delete_pro_offer/<int:id>/',views.delete_pro_offer,name='delete_pro_offer'),
    path('view_review/',views.review_rating_view,name='view_review'),
    path('review_block/<int:id>/',views.review_block,name='review_block'),
    path('review_unblock/<int:id>/',views.review_unblock,name='review_unblock'),
    path('add_coupen/',views.add_coupen,name='add_coupen')
    
   
    


]
