from django.shortcuts import render, redirect

from cart.models import Cart
from .models import Order, OrderItem


def checkout(request):

    cart = None

    if request.session.session_key:

        try:
            cart = Cart.objects.get(
                session_key=request.session.session_key,
                status="active"
            )

        except Cart.DoesNotExist:
            pass


    if request.method == "POST":

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            total=cart.grand_total,
            status="pending"
        )


        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )


        cart.items.all().delete()


        return redirect("order_success")


    return render(
        request,
        "orders/checkout_page.html",
        {
            "cart": cart
        }
    )
def order_success(request):

    return render(
        request,
        "orders/success.html"
    )

from django.shortcuts import get_object_or_404


def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order
        }
    )