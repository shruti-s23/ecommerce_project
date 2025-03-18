from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def setUp(self):
        Product.objects.create(
            name="Test Product",
            description="This is a test product",
            price=19.99,
            stock=10
        )

    def test_product_creation(self):
        product = Product.objects.get(name="Test Product")
        self.assertEqual(product.price, 19.99)
        self.assertEqual(product.stock, 10)
        self.assertEqual(str(product), "Test Product")
