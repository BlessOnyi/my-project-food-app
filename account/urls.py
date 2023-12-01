
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




app_name ='account'
urlpatterns = [
    path('register',views.register_user, name='register_user'),
    path('login',views.login_view, name='login'),
    path('dashboard_account', views.dashboard_account, name='dashboard_account'), 
    path('change_form', views.change_form, name='change_form'), 
    path('logout_view', views.logout_view, name='logout_view'),
    path('basic',views.basic, name='basic'),
    path('user_profile',views.user_profile, name='user_profile'),
    path('edit_form',views.edit_form, name='edit_form'),
]