from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# 🍲 Dish Model - Represents Menu Items
from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100, verbose_name="Dish Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Price")
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True, verbose_name="Dish Image")
    available = models.BooleanField(default=True, verbose_name="Available")

    def __str__(self):
        return self.name

    category_choices = [
        ('Starters', 'Starters'),
        ('Main Course', 'Main Course'),
        ('Drinks', 'Drinks'),
        ('Desserts', 'Desserts'),
    ]
    category = models.CharField(max_length=20, choices=category_choices)

    def __str__(self):
        return self.name





# 🛒 Cart Model - Holds User's Cart
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cart for {self.user.username}"


# 🛍️ CartItem Model - Items in Cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,)
    dish = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.dish.price

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"


# 🚚 Order Model - Stores User Orders
class Order(models.Model):
    customer_name = models.CharField(max_length=100, default="Guest")
    customer_address = models.TextField(default="Default Address")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status_choices = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=order_status_choices, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"


# 📦 OrderItem - Correct Intermediary Model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(MenuItem, on_delete=models.CASCADE, default=1)  
    quantity = models.PositiveIntegerField(default=1)


    def total_price(self):
        return self.quantity * self.dish.price

    def __str__(self):
        return f"{self.quantity} x {self.dish.name} in Order {self.order.id}"


# 💳 Payment Model - Stores Payment Info

class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('gpay', 'Google Pay'),
        ('phonepe', 'PhonePe'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    paid_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_method} - Order #{self.order.id}"
