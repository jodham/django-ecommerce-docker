from django.urls import path

from .views import checkout, order_detail, order_success


urlpatterns = [
    path("", checkout,  name="checkout"),
    path("success/<int:order_id>/", order_success, name="order_success"),
    path("<int:order_id>/", order_detail, name="order_detail"),
]