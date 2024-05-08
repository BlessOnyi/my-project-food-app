from django.shortcuts import render
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
import requests
from ProjectApp.models import Products
from basket.basket import *
from django.http import HttpResponseRedirect, JsonResponse
from orders.models import *
import json

@login_required(login_url='/account/login/')
def payment_completed(request):
    # Get the reference from the request body
    reference = request.POST.get('reference')

    # Verify the transaction with Paystack
    headers = {'Authorization': 'Bearer {{sk_test_efea5c7d713b390d867c1d6bd4575b7160a72184 }}'}
    
    response = requests.get('https://api.paystack.co/transaction/verify/' , reference, headers=headers)

    # Get the transaction data from the response
    transaction_data = response.json().get('data')

    # Get the order total
    # total_paid = transaction_data.get('amount') / 100

    # Create the order and save it to the database
    # order = Order.objects.create(
    #     # user=user_id,
    #     full_name=transaction_data.get('metadata').get('full_name'),
    #     email=transaction_data.get('customer').get('email'),
    #     address1=transaction_data.get('metadata').get('address'),
    #     city=transaction_data.get('metadata').get('city'),
    #     postal_code=transaction_data.get('metadata').get('postal_code'),
    #     country_code=transaction_data.get('metadata').get('country'),
    #     # total_paid=total_paid,
    #     payment_option='Paystack',
    #     payment_id=reference,
    #     billing_status=True
    # )

    # Create the order items and save them to the database

    # for item in basket:
    #     OrderItem.objects.create(
    #         order=order,
    #         product=item['product'],
    #         price=item['price'],
    #         quantity=item['qty']
    #     )
    return render(request, 'payment/payment.html')

@login_required(login_url='/account/login/')
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    
    purchased_product_ids = request.session.get('purchased_product_ids', [])
    products = Products.objects.filter(id__in=purchased_product_ids)
      # Debugging code
    print(products) # Check if any products are returned
    
    context = {
        'products': products
    }
    
    return render(request, "payment/payment_successful.html",context)
