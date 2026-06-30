from django.shortcuts import render

from django.db.models import Sum, Count

from orders.models import Order

from products.models import Product

from inventory.models import InventoryTransaction

from django.db import models

from django.db.models.functions import TruncDate

def dashboard(request):


    total_orders = Order.objects.count()


    total_revenue = Order.objects.filter(

        payment_status="paid"

    ).aggregate(

        total=Sum("total")

    )["total"] or 0



    paid_orders = Order.objects.filter(

        payment_status="paid"

    ).count()



    low_stock_products = Product.objects.filter(

        stock_quantity__lte=models.F(
            "low_stock_threshold"
        ),

        stock_quantity__gt=0

    )


    out_of_stock_products = Product.objects.filter(

        stock_quantity=0

    )


    recent_transactions = InventoryTransaction.objects.select_related(

        "product"

    ).order_by(

        "-created_at"

    )[:10]
    recent_orders = Order.objects.filter(
        payment_status="paid"
        ).order_by(
        "-created_at"
        )[:5]

    sales_data = (

        Order.objects.filter(
            payment_status="paid"
        )

        .annotate(
            date=TruncDate("created_at")
        )

        .values("date")

        .annotate(
            revenue=Sum("total")
        )

        .order_by("date")

    )

    context = {

        "sales_data": sales_data,

        "recent_orders": recent_orders,

        "total_orders": total_orders,

        "total_revenue": total_revenue,

        "paid_orders": paid_orders,

        "low_stock_products": low_stock_products,

        "out_of_stock_products": out_of_stock_products,

        "recent_transactions": recent_transactions,

    }



    return render(

        request,

        "dashboard/index.html",

        context

    )