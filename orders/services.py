import uuid

from django.utils import timezone
from .models import Payment



def initialize_payment(order):

    payment_reference = (
        f"PAY-{uuid.uuid4().hex[:8].upper()}"
    )


    Payment.objects.create(

        order=order,

        amount=order.total,

        payment_method="mock",

        transaction_reference=payment_reference,

        status="pending"

    )


    order.payment_status = "pending"

    order.payment_method = "mock"

    order.transaction_id = payment_reference

    order.save()


    return {

        "success": True,

        "transaction_id": payment_reference,

        "message": "Payment initialized",

        "order": order

    }


def confirm_payment(order):

    payment = order.payments.last()


    if payment:

        payment.status = "paid"

        payment.save()


    order.payment_status = "paid"

    order.paid_at = timezone.now()

    order.save()


    return {

        "success": True,

        "message": "Payment confirmed",

        "order": order

    }

def retry_payment(order):

    payment_reference = (
        f"PAY-{uuid.uuid4().hex[:8].upper()}"
    )


    payment = Payment.objects.create(

        order=order,

        amount=order.total,

        payment_method="mock",

        transaction_reference=payment_reference,

        status="pending"

    )


    order.payment_status = "pending"

    order.payment_method = "mock"

    order.transaction_id = payment_reference

    order.save()


    return {

        "success": True,

        "transaction_id": payment_reference,

        "payment": payment

    }