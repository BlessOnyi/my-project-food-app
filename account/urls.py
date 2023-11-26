
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




app_name ='account'
urlpatterns = [
    path('register',views.register_user, name='register_user'),
    path('login',views.login_view, name='login'),
    
]