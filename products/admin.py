from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (

        "name",

        "price",

        "stock_quantity",

        "stock_status",
        "stock",
        "created_at"

    )


    search_fields = (

        "name",

    )
