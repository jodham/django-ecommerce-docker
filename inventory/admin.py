from django.contrib import admin
from .models import InventoryTransaction

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):

    list_display = (

        "product",

        "quantity",

        "transaction_type",

        "reference",

        "created_at",

    )


    list_filter = (

        "transaction_type",

    )