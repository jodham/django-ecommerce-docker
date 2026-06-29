from django.db import models
from django.conf import settings
import uuid
from products.models import Product


class Order(models.Model):
    order_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    customer_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    PAYMENT_STATUS_CHOICES = [

        ("unpaid", "Unpaid"),

        ("paid", "Paid"),

        ("failed", "Failed"),

        ("refunded", "Refunded"),

    ]
    STATUS_CHOICES = [

        ("pending", "Pending"),

        ("confirmed", "Confirmed"),

        ("processing", "Processing"),

        ("packed", "Packed"),

        ("shipped", "Shipped"),

        ("delivered", "Delivered"),

        ("cancelled", "Cancelled"),

    ]


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    payment_status = models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS_CHOICES,

        default="unpaid"

    )

    payment_method = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    
    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True
    )


    paid_at = models.DateTimeField(
        blank=True,
        null=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    stock_deducted = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.order_number:

            self.order_number = (
                f"LXC-{uuid.uuid4().hex[:6].upper()}"
            )

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Order {self.id}"



class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    @property
    def subtotal(self):
        return self.price * self.quantity


    def __str__(self):
        return self.product.name
    

class Payment(models.Model):

    PAYMENT_STATUS_CHOICES = [

        ("pending", "Pending"),

        ("paid", "Paid"),

        ("failed", "Failed"),

        ("refunded", "Refunded"),

    ]


    order = models.ForeignKey(

        Order,

        related_name="payments",

        on_delete=models.CASCADE

    )


    amount = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    attempt_number = models.PositiveIntegerField(
        default=1
    )


    payment_method = models.CharField(

        max_length=50

    )


    status = models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS_CHOICES,

        default="pending"

    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        null=True
    )

    transaction_reference = models.CharField(

        max_length=100,

        unique=True

    )

    checkout_request_id = models.CharField(

        max_length=100,

        blank=True,

        null=True

    )


    created_at = models.DateTimeField(

        auto_now_add=True

    )


    updated_at = models.DateTimeField(

        auto_now=True

    )


    def __str__(self):

        return self.transaction_reference