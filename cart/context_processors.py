from .models import Cart


def cart_count(request):

    count = 0

    if request.session.session_key:

        try:
            cart = Cart.objects.get(
                session_key=request.session.session_key,
                status="active"
            )

            count = sum(
                item.quantity
                for item in cart.items.all()
            )

        except Cart.DoesNotExist:
            pass

    return {
        "cart_count": count
    }