from django.shortcuts import render
from account.token import *
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
from django.contrib.auth.forms import PasswordChangeForm
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



def register_user(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            print('the form')
            # Create a user object with the form data, but don't save it to the database yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Ensure that the user object is not None before accessing attributes
        
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
            # Handle the case where user or user.is_active is None
            return render(request, 'error_template.html', {'error_message': 'User activation failed'})

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
            return redirect('ProjectApp:myHome')
        else:
            messages.error(request, 'Username and Password do not match')
    return render(request, 'forms/login.html')
