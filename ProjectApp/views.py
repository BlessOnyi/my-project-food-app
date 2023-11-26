
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
        # multiple_search = Q(Q(title__icontains=searched) | Q(description__icontains=searched))
        # products = Products.objects.filter(multiple_search)
    return render (request, 'index.html', {'products':products,'categories':categories})
    


def product_detail(request, slug):
    product = get_object_or_404(Products, slug=slug, in_stock=True)
    return render(request, 'post_detail.html',{'product': product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug =category_slug)
    products = Products.objects.filter(category=category)
    return render (request, 'category.html',{'category':category, 'products':products})




@login_required
def pass_form(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(data=request.POST,user=request.user)
        if pass_form.is_valid():
            pass_form.save()
            update_session_auth_hash(request, pass_form.user)
            messages.success(request, 'password changed succesfully')
    else:
        pass_form=PasswordChangeForm(user=request.user)
    return render(request, 'change-password.html', {'pass_key':pass_form})

# def about(request):
#     return render (request, 'about.html')

# def menu(request):
#     return render (request, 'menu.html')

# def booking(request):
#     return render (request, 'book.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'forms/password_reset.html'
    email_template_name = 'forms/password_reset_email.html'
    subject_template_name = 'forms/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('ProjectApp:login')