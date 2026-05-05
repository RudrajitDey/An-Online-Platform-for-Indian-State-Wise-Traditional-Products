from django.db import models
from django.conf import settings
from Home.models import Product
from Home.models import Product



# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    cart_id = models.CharField(max_length=250, blank=True, null=True)

    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def total_price(self):
        return self.product.price * self.quantity

    def get_product(self):
        return self.product

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"