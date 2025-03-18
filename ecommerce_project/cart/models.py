from django.db import models
from django.contrib.auth.models import User
from shop.models import Product  

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow guest users (null)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)
    session_id = models.CharField(max_length=50, null=True, blank=True)  # Store session ID for guests

    def total_price(self):
        return self.product.price * self.quantity if self.product.price else 0

    def __str__(self):
        user_info = self.user.username if self.user else f"Guest ({self.session_id})"
        return f"{user_info} - {self.quantity} x {self.product.name} (${self.total_price():.2f})"

    @staticmethod
    def add_to_cart(user, session_id, product):
        """Adds a product to the cart or increases quantity if it already exists."""
        if user:
            cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        else:
            cart_item, created = Cart.objects.get_or_create(session_id=session_id, product=product)

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    @staticmethod
    def remove_from_cart(user, session_id, product):
        """Removes one instance of a product from the cart, deletes if quantity = 1."""
        if user:
            cart_item = Cart.objects.filter(user=user, product=product).first()
        else:
            cart_item = Cart.objects.filter(session_id=session_id, product=product).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
