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
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name