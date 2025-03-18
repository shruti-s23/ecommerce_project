from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart
from shop.models import Product  # Import Product model
from django.contrib import messages

def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(session_id=request.session.session_key)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})

def update_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first() if request.user.is_authenticated else Cart.objects.filter(session_id=request.session.session_key, product=product).first()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
            else:
                Cart.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_id=request.session.session_key,
                    product=product,
                    quantity=1
                )

        elif action == "remove":
            if cart_item:
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()

    return redirect("view_cart")

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user if request.user.is_authenticated else None,
        session_id=request.session.session_key,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"✅ {product.name} added to cart!")
    return redirect('view_cart')

def checkout(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = Cart.objects.filter(session_id=request.session.session_key)

    total_price = sum(item.total_price() for item in cart_items)

    if not cart_items:
        messages.warning(request, "🛒 Your cart is empty!")
        return redirect('view_cart')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})

def order_details(request):
    return render(request, 'order_details.html')

def complete_purchase(request):
    if request.method == "POST":
        # Ensure the session exists for guest users
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key

        # Clear the cart after purchase
        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user).delete()
        else:
            Cart.objects.filter(session_id=session_id).delete()

        messages.success(request, "🎉 Your order has been placed successfully!")
        return redirect('order_confirmation')  # Redirect to confirmation page

    return redirect('view_cart')  # If accessed directly, go back to cart

def order_confirmation(request):
    return render(request, 'order_confirmation.html')
