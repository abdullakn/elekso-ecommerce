
from django.urls import path
from . import views

urlpatterns = [
  path('place_order/',views.place_order,name='place_order'),
  path('payments/',views.payments,name='payments'),
  path('pay_option',views.pay_option,name='pay_option'),
  path('invoice/',views.invoice,name='invoice'),
  path('payment_complete',views.payment_complete,name='payment_complete'),
  path('razorpay',views.razorpay,name='razorpay')
]
