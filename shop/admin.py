from django.contrib import admin
from shop.models import Cart, CartItem, Order, OrderItem, Payment,MenuItem

# Register Models
admin.site.register(MenuItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
