from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import cart
from .services import initialize_payment, retry_payment, initiate_mpesa_payment
from cart.models import Cart
from .models import Order, OrderItem, Payment
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

@login_required
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

    if not cart or not cart.items.exists():

        return redirect("cart_detail")


    if request.method == "POST":



        order = Order.objects.create(

            user=request.user if request.user.is_authenticated else None,

            customer_name=request.POST.get("first_name") + " " + request.POST.get("last_name"),

            email=request.POST.get("email"),

            phone=request.POST.get("phone"),

            address=request.POST.get("address"),

            city=request.POST.get("city"),

            country=request.POST.get("country"),

            total=cart.grand_total,

        )


        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.status = "completed"
        cart.save()


        payment = initiate_mpesa_payment(

            order,

            request.POST.get("phone")

        )
        return redirect(

            "payment_pending",

            order_number=order.order_number

        )
        


    return render(
        request,
        "orders/checkout_page.html",
        {
            "cart": cart
        }
    )
@login_required
def order_success(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number
    )
    return render(
        request,
        "orders/success.html",
        {
            "order": order
        }
    )

@login_required
def order_detail(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number
    )

    status_steps = [
        "pending",
        "confirmed",
        "processing",
        "packed",
        "shipped",
        "delivered",
    ]

    current_index = status_steps.index(order.status)
    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order,
            "status_steps": status_steps,
            "current_index": current_index
        }
        
    )

@login_required
def order_history(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")


    return render(
        request,
        "orders/order_history.html",
        {
            "orders": orders
        }
    )

@login_required
def retry_mpesa_payment(request, order_number):


    order = get_object_or_404(

        Order,

        order_number=order_number,

        user=request.user

    )



    payment = initiate_mpesa_payment(

        order,

        order.phone

    )



    return redirect(

        "payment_pending",

        order_number=order.order_number

    )

id="mpesa_callback_view"
@csrf_exempt
def mpesa_callback(request):


    data = request.json if hasattr(request, "json") else None


    body = request.body.decode("utf-8")


    import json

    payload = json.loads(body)



    callback = payload.get(
        "Body",
        {}
    ).get(
        "stkCallback",
        {}
    )



    checkout_request_id = callback.get(
        "CheckoutRequestID"
    )



    result_code = callback.get(
        "ResultCode"
    )



    try:

        payment = Payment.objects.get(

            checkout_request_id=checkout_request_id

        )


    except Payment.DoesNotExist:


        return JsonResponse(

            {
                "message":
                "Payment not found"

            },

            status=404

        )



    if result_code == 0:


        callback_metadata = {}



        items = callback.get(
            "CallbackMetadata",
            {}
        ).get(
            "Item",
            []
        )



        for item in items:


            callback_metadata[
                item.get("Name")
            ] = item.get("Value")



        payment.status = "paid"



        payment.metadata = callback_metadata



        payment.save()



        order = payment.order


        order.payment_status = "paid"

        order.payment_method = "M-Pesa"

        order.transaction_id = (
            callback_metadata.get(
                "MpesaReceiptNumber"
            )
        )

        order.paid_at = timezone.now()


        order.save()



    else:


        callback_metadata = {}


        items = callback.get(
            "CallbackMetadata",
            {}
        ).get(
            "Item",
            []
        )


        for item in items:

            callback_metadata[
                item.get("Name")
            ] = item.get("Value")



        payment.status = "failed"


        payment.metadata = callback_metadata


        payment.save()



        order = payment.order


        order.payment_status = "failed"


        order.save()



    return JsonResponse(

        {
            "ResultCode": 0,

            "ResultDesc":
            "Accepted"

        }

    )

@login_required
def payment_status(request, order_number):

    order = get_object_or_404(

        Order,

        order_number=order_number,

        user=request.user

    )


    payment = order.payments.order_by(
        "-created_at"
    ).first()



    return JsonResponse({

        "status":
            payment.status

    })

@never_cache
@login_required
def payment_pending(request, order_number):

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user
    )


    payment = order.payments.order_by(
        "-created_at"
    ).first()


    if payment.status == "paid":

        return redirect(
            "order_success",
            order_number=order.order_number
        )


    return render(
        request,
        "orders/payment_pending.html",
        {
            "order": order
        }
    )

@login_required
def payment_failed(request, order_number):


    order = get_object_or_404(

        Order,

        order_number=order_number,

        user=request.user

    )


    return render(

        request,

        "orders/payment_failed.html",

        {
            "order": order
        }

    )