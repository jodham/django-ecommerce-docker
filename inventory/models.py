from django.db import models
from products.models import Product


class InventoryTransaction(models.Model):

    TRANSACTION_TYPES = (

        ("sale", "Sale"),

        ("restock", "Restock"),

    )


    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE,

        related_name="inventory_transactions"

    )


    quantity = models.IntegerField()


    transaction_type = models.CharField(

        max_length=20,

        choices=TRANSACTION_TYPES

    )


    reference = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    def __str__(self):

        return f"{self.product.name} - {self.quantity}"