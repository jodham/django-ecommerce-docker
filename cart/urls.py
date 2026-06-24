from django.urls import path

from .views import add_to_cart, cart_detail, checkout, update_quantity, remove_item, clear_cart


urlpatterns = [
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("", cart_detail, name="cart_detail"),
    path("update/<int:item_id>/<str:action>/", update_quantity, name="update_quantity"),
    path("remove/<int:item_id>/", remove_item, name="remove_item"),
    path("clear/", clear_cart, name="clear_cart"),
]