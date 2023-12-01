
from django.shortcuts import get_object_or_404, render,redirect
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

# from django.db.models import Q


# Create your views here.

def myHome(request):
 
    products = Products.objects.all()
    categories = Category.objects.all()

    # Check if a category is selected
    selected_category = request.GET.get('category')
    searched = request.POST.get('searched')

    if selected_category:
        # Filter food items by the selected category
        products = Products.objects.filter(category__slug=selected_category)
        return products
    elif searched:
        products = Products.objects.filter(title__icontains=searched)
       
    return render (request, 'index.html', {'products':products,'categories':categories})




def product_detail(request, slug):
    product = get_object_or_404(Products, slug=slug, in_stock=True)
    return render(request, 'post_detail.html',{'product': product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug =category_slug)
    products = Products.objects.filter(category=category)
    return render (request, 'category.html',{'category':category, 'products':products})



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'forms/password_reset.html'
    email_template_name = 'forms/password_reset_email.html'
    subject_template_name = 'forms/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('account:login')



# class PasswordResetConfirmView():
   
#    success_url = reverse_lazy("ProjectApp:password_reset_complete")