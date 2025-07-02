from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart,OrderItem,Order,CartItem,Payment, MenuItem
from django.contrib.auth.decorators import login_required
import stripe
from .models import MenuItem, Cart, CartItem, Order
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import PaymentForm

import stripe
from django.conf import settings
from django.core.files.storage import default_storage
from .models import Order



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # 🛑 Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        # ⚡ Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        # ✅ Create and save the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'register.html')


# 🔐 Login User
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # 🧩 Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user) 
            messages.success(request, f"Welcome back, {username}!")
            return redirect('index')  # Redirect to home or dashboard
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

    return render(request, 'login.html')


# 🚪 Logout User
def logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')




# Homepage - Browse Menu
def index(request):
    foods = MenuItem.objects.all()
    return render(request, 'index.html', {'foods': foods})


def menu(request):
    dishes = MenuItem.objects.all()
    
    for dish in dishes:
        if not dish.image or not default_storage.exists(dish.image.name):
            dish.image_url = '/static/images/default_image.jpg'
        else:
            dish.image_url = dish.image.url

    context = {'dishes': dishes}
    return render(request, 'menu.html', context)



# 🍲 Dish Details - Individual Dish View
def dish_detail(request, id):
    dish = get_object_or_404(MenuItem, id=id)
    return render(request, 'dish_detail.html', {'dish': dish})






# Cart Page
@login_required
def cart(request):
    return render(request, 'cart.html')

# Checkout with Stripe Payment
@login_required
def checkout(request):
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_amount=100.00,  # This will be calculated dynamically
            payment_status='Pending',
            order_status='Pending'
        )
        # Redirect to success page
        return redirect('order_history')

    return render(request, 'checkout.html')

# Order History
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_history.html', {'orders': orders})



# 🛒 View Cart
def cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


# ➕ Add to Cart
def add_to_cart(request, dish_id):
    dish = get_object_or_404(MenuItem, id = dish_id)
    quantity = int(request.POST.get('quantity', 1))
 # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        dish=dish
    )
    
    # If the item already exists, increase quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# ❌ Remove from Cart
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



from django.shortcuts import render, get_object_or_404, redirect
from .models import MenuItem, Order, OrderItem

def order_detail(request, dish_id):
    dish = get_object_or_404(MenuItem, id=dish_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        # Create a new order or get an existing one (for simplicity, using guest order)
        order = Order.objects.create(customer_name="Guest")
        OrderItem.objects.create(order=order, food_item=dish, quantity=quantity)

        return redirect('checkout')  # or show order summary

    return render(request, 'shop/order_detail.html', {'dish': dish})





def checkout(request):
    if request.method == 'POST':
        # Save the order from form/cart
        order = Order.objects.create(
            customer_name='John Doe',
            phone='9999999999',
            address='Somewhere',
            total_amount=999.99
        )
        return redirect('make_payment', order_id=order.id)
    return render(request, 'checkout.html')




# Payment Failed
def payment_failed(request):
    return render(request, 'shop/payment_failed.html')








def make_payment(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.order = order
            payment.save()
            order.payment_status = 'Paid'
            order.save()
            return redirect('payment_success')
    else:
        form = PaymentForm()

    return render(request, 'shop/payment.html', {'form': form, 'order': order})




stripe.api_key = settings.STRIPE_SECRET_KEY





def payment_success(request):
    # Create order after successful payment
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()

    if cart_items.exists():
        order = Order.objects.create(user=request.user, total_price=sum(item.dish.price * item.quantity for item in cart_items))
        
        # Add items to order
        for item in cart_items:
            OrderItem.objects.create(order=order, dish=item.dish, quantity=item.quantity)
        
        # Clear cart after order is placed
        cart_items.delete()

    return render(request, 'payment_success.html')