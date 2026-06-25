from django.urls import path

from .views import checkout, order_detail, order_history, order_success


urlpatterns = [
    path("", checkout,  name="checkout"),
    path("success/<str:order_number>/", order_success, name="order_success"),
    path("detail/<str:order_number>/", order_detail, name="order_detail"),
    path("account/orders/", order_history, name="order_history"),
]