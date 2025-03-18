from django.urls import path
from .views import home, products_list, product_detail, add_to_cart, view_cart, remove_from_cart, checkout

urlpatterns = [
    path('', home, name='home'),
    path('products/', products_list, name='products_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]
