from django.shortcuts import get_object_or_404, render

from .models import Product


def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        "products/product_list.html",
        {"products": products}
    )

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(
        request,
        "products/product_detail.html",
        {"product": product}
    )