from django.contrib import admin

from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_name",
        "status",
        "payment_status",
        "total",
        "created_at",
    )

    list_filter = (
        "status",
        "payment_status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "customer_name",
        "email",
        "phone",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "order_number",
        "created_at",
        "paid_at",
    )
    fieldsets = (

        (
            "Order Information",
            {
                "fields": (
                    "order_number",
                    "customer_name",
                    "email",
                    "phone",
                    "address",
                    "city",
                    "country",
                )
            }
        ),


        (
            "Fulfillment",
            {
                "fields": (
                    "status",
                )
            }
        ),


        (
            "Payment",
            {
                "fields": (
                    "payment_status",
                    "payment_method",
                    "transaction_id",
                    "paid_at",
                )
            }
        ),


        (
            "Totals",
            {
                "fields": (
                    "total",
                    "created_at",
                )
            }
        ),

    )

    inlines = [
        OrderItemInline
    ]



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (
        "order",
        "product",
        "quantity",
        "price",
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (

        "transaction_reference",

        "order",

        "attempt_number",

        "amount",

        "status",

        "payment_method",

        "created_at",

    )


    list_filter = (

        "status",

        "payment_method",

        "created_at",

    )


    search_fields = (

        "transaction_reference",

        "order__order_number",

    )