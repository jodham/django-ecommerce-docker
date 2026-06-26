from django.urls import path

from .views import checkout, order_detail, order_history, order_success, retry_payment_view


urlpatterns = [
    path("", checkout,  name="checkout"),
    path("success/<str:order_number>/", order_success, name="order_success"),
    path("detail/<str:order_number>/", order_detail, name="order_detail"),
    path("account/orders/", order_history, name="order_history"),
    path("retry-payment/<str:order_number>/", retry_payment_view, name="retry_payment"),
]