from django.db import models
from django.conf import settings

from products.models import Product


class Cart(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    session_key = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        default="active"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"Cart {self.id}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    def __str__(self):
        return self.product.name