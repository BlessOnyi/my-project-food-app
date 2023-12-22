from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from ProjectApp.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import login, logout, authenticate
from ProjectApp.forms import RegForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .token import account_activation_token



from django.http import HttpResponseServerError

def register_user(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            print('valid entry')
            # Create a user object with the form data, but don't save it to the database yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Ensure that the user object is not None before accessing attributes
            if user is not None:
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('account/activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                
                return redirect('activation_sent')
            else:
                print('User is None. Form data may be invalid.')
                print(form.errors)
        else:
            print('Form is not valid.')
            print(form.errors)
    else:
        form = RegForm()
    return render(request, 'forms/register.html', {'reg_form': form})




def activation_sent_view(request):
    return render(request, 'account/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:login')
    else:
        return render(request, 'account/activation_invalid.html')
    

    

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account:dashboard_account')
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request, 'forms/login.html')


def dashboard_account(request):
    
    return render (request,'dashboard/index.html' )



def logout_view(request):
    logout(request)
    return redirect('account:login')

def basic(request):
    return render(request, 'dashboard/basic_elements.html')



@login_required(login_url='/account/login/')
def change_form(request):
    if request.method == 'POST':
        change_form = PasswordChangeForm(data=request.POST,user=request.user)
        if change_form.is_valid():
            change_form.save()
            update_session_auth_hash(request, change_form.user)
            messages.success(request, 'password changed succesfully')
    else:
        change_form=PasswordChangeForm(user=request.user)
    return render(request, 'dashboard/changepassword.html', {'pass_key':change_form})



@login_required(login_url='/account/login/')
def user_profile(request):
    # my_user = User.objects.filter(user=request.user)
    return render(request, 'dashboard/user-profile.html', {'profile':request.user})


@login_required(login_url='/account/login/')
def edit_form(request):
    if request.method == 'POST':
        edit_form = EditUserForm(request.POST, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, 'User edited successfully.')
    else:
        edit_form = EditUserForm(instance=request.user)
    return render(request, 'dashboard/edit-user-profile.html', {'edit_key':edit_form})



def blog_form(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.user = request.user
            blog.save()
            messages.success(request, 'Blog Posted')
    else:
        blog_form = BlogForm()
    return render(request, 'blog/add-blog.html', {'blog': blog_form})