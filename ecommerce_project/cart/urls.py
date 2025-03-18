from django.urls import path
from .views import add_to_cart, view_cart, checkout, complete_purchase, order_confirmation, order_details, update_cart

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('update/<int:product_id>/', update_cart, name='update_cart'),  # ✅ ADDED update_cart
    path('view/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order-details/', order_details, name='order_details'),
    path('complete_purchase/', complete_purchase, name='complete_purchase'),
    path('order-confirmation/', order_confirmation, name='order_confirmation'),
]
