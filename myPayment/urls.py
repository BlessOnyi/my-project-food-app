from django.urls import path
from . import views


app_name ='myPayment'

urlpatterns = [
    path("payment_completed/", views.payment_completed, name="payment_completed"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
]