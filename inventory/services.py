from .models import InventoryTransaction


def reduce_stock_for_order(order):

    for item in order.items.all():

        product = item.product


        product.stock_quantity -= item.quantity

        product.save()



        InventoryTransaction.objects.create(

            product=product,

            quantity=-item.quantity,

            transaction_type="sale",

            reference=order.order_number

        )


def restock_product(product, quantity):

    product.stock_quantity += quantity

    product.save()


    InventoryTransaction.objects.create(

        product=product,

        quantity=quantity,

        transaction_type="restock",

        reference="Admin Restock"

    )