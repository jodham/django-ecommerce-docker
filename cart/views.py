from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from products.models import Product

from .models import Cart, CartItem


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if not product.is_in_stock:

        return redirect("product_list")
    # Ensure guest users have a session
    if not request.session.session_key:

        request.session.create()



    cart = Cart.objects.filter(
        session_key=request.session.session_key,
        status="active"
    ).first()



    if not cart:

        cart = Cart.objects.create(
            session_key=request.session.session_key,
            status="active"
        )



    cart_item, created = CartItem.objects.get_or_create(

        cart=cart,

        product=product

    )


    if not created:


        if cart_item.quantity + 1 > product.stock_quantity:

            return redirect(
                "cart_detail"
            )


        cart_item.quantity += 1


    else:


        cart_item.quantity = 1


    cart_item.save()


    return redirect("product_list")

def cart_detail(request):

    cart = None

    if request.session.session_key:

        try:
            cart = Cart.objects.get(
                session_key=request.session.session_key,
                status="active"
            )

        except Cart.DoesNotExist:
            pass
   
    return render(
        request,
        "cart/cart_detail.html",
        {"cart": cart}
    )

def update_quantity(request, item_id, action):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if action == "increase":

        item.quantity += 1

    elif action == "decrease":

        if item.quantity > 1:
            item.quantity -= 1

    item.save()

    return redirect("cart_detail")

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

    return render(
        request,
        "cart/checkout_page.html",
        {"cart": cart}
    )

def remove_item(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    item.delete()

    return redirect("cart_detail")

def clear_cart(request):

    if request.session.session_key:

        try:
            cart = Cart.objects.get(
                session_key=request.session.session_key,
                status="active"
            )

            cart.items.all().delete()

        except Cart.DoesNotExist:
            pass


    return redirect("cart_detail")