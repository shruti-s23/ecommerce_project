from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from cart.models import Cart

def get_cart_items(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)
    else:
        session_id = request.session.session_key
        return Cart.objects.filter(session_id=session_id) if session_id else Cart.objects.none()

def home(request):
    products = Product.objects.all()
    cart_items = get_cart_items(request)
    total_cart_price = sum(item.total_price() for item in cart_items)
    cart_item_count = sum(item.quantity for item in cart_items)

    return render(request, 'home.html', {
        'products': products,
        'total_cart_price': total_cart_price,
        'cart_item_count': cart_item_count,
    })

def products_list(request):
    products = Product.objects.all()
    return render(request, 'products_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        cart_item, created = Cart.objects.get_or_create(product=product, session_id=session_id)

    if not created:
        cart_item.quantity += 1
    cart_item.save()
    
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart_item = get_cart_items(request).filter(product_id=product_id).first()
    
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('view_cart')

def view_cart(request):
    cart_items = get_cart_items(request)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout(request):
    cart_items = get_cart_items(request)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total_price': total_price})
