
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
from django.contrib.auth import views as auth_views

# from django.db.models import Q


# Create your views here.

def myHome(request):
 
    products = Products.objects.all()
    categories = Category.objects.all()

    # Check if a category is selected
    selected_category = request.GET.get('category')
    searched = request.POST.get('q')

    if selected_category:
        # Filter food items by the selected category
        products = Products.objects.filter(category__slug=selected_category)
        return products
    elif searched:
        products = Products.objects.filter(title__icontains=searched)
       
    return render (request, 'index.html', {'products':products,'categories':categories})

def product_all(request):
    products = Products.objects.all()
    return render(request, 'home.html', {'products': products})



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



# def password_reset_confirm(request, uidb64, token):
    
#     try:
#         # Decode the uidb64 to get the user's ID
#         user = auth_views.uidb64_decode(uidb64)

#         response = auth_views.PasswordResetConfirmView.as_view(
#             template_name='form/password_reset_confirm.html'
#         )(request, uidb64=uidb64, token=token)

#         if response.status_code == 200 and request.method == 'POST':
#             messages.success(request, 'Password successfully reset.')
#             return redirect('password_reset_complete')  # Replace with your actual success view name

#         return response

#     except Exception as e:
#         # Handle any exceptions that may occur during the process
#         messages.error(request, 'An error occurred during password reset.')
#         return redirect('login')  # Replace with your actual error view name
def mycontact(request):
    return render(request,'contact.html')