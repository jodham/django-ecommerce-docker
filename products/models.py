from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to='images/products/',
        blank=True,
        null=True
    )

    stock_quantity = models.PositiveIntegerField(
        default=0
    )


    low_stock_threshold = models.PositiveIntegerField(
        default=5
    )
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @property
    def stock_status(self):

        if self.stock_quantity == 0:

            return "Out of Stock"


        if self.stock_quantity <= self.low_stock_threshold:

            return "Low Stock"


        return "Available"
    
    @property
    def is_in_stock(self):

        return self.stock_quantity > 0

    def __str__(self):
        return self.name