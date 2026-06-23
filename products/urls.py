from django.urls import path

from .views import home, product_detail, product_list


urlpatterns = [
    path("product_list/", product_list, name="product_list"),

    path(
        "<int:id>/", product_detail, name="product_detail"
    ),
    path("", home, name="home")
]