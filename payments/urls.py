# payments/urls.py
from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path("checkout/", views.create_checkout, name="checkout"),
    path("initialize/", views.api_initialize, name="initialize"),
    path("verify/", views.verify, name="verify"),
    path("webhook/", views.webhook, name="webhook"),
]
