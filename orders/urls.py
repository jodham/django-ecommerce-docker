from django.urls import path

from .views import checkout, order_detail, order_history, order_success, retry_mpesa_payment, mpesa_callback, payment_status, payment_pending, payment_failed
             

urlpatterns = [
    path("", checkout,  name="checkout"),
    path("success/<str:order_number>/", order_success, name="order_success"),
    path("detail/<str:order_number>/", order_detail, name="order_detail"),
    path("account/orders/", order_history, name="order_history"),
    path("retry-payment/<str:order_number>/", retry_mpesa_payment, name="retry_mpesa_payment"),
    path("mpesa/callback/", mpesa_callback, name="mpesa_callback"),
    path("payment-status/<str:order_number>/", payment_status, name="payment_status"),
    path("payment-pending/<str:order_number>/", payment_pending, name="payment_pending"),
    path("payment-failed/<str:order_number>/", payment_failed, name="payment_failed"),
   
]