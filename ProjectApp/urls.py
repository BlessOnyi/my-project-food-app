from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from ProjectApp.views import ResetPasswordView


app_name ='ProjectApp'
urlpatterns = [
    path('', views.myHome, name='myHome'),
    path('item/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search/<slug:category_slug>', views.category_list, name='category_list'),
    path('search_food', views.myHome, name='search_food'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='forms/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='forms/password_reset_complete.html'),name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='forms/password_reset_confirm.html'),name='password_reset_confirm'),
    # path('about', views.about, name='about'),
    # path('menu', views.menu, name='menu'),
    # path('booking', views.booking, name='booking'),   
]