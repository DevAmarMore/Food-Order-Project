from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('', views.register, name='register'),
    path('index/', views.index, name='index'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add_to_cart/<int:dish_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('menu/', views.menu, name='menu'),
    path('dish/<int:id>/', views.dish_detail, name='dish_detail'),
    path('order-history/', views.order_history, name='order_history'),  
    path('payment/<int:order_id>/', views.make_payment, name='make_payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
   path('order/', views.order_detail, name='order_food'),
]

