
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views




app_name ='account'
urlpatterns = [
    path('register/',views.register_user, name='register_user'),
    path('login/',views.login_view, name='login'),
    path('dashboard_account/', views.dashboard_account, name='dashboard_account'), 
    path('change_form/', views.change_form, name='change_form'), 
    path('logout_view/', views.logout_view, name='logout_view'),
    path('basic/',views.basic, name='basic'),
    path('user_profile/',views.user_profile, name='user_profile'),
    path('edit_form/',views.edit_form, name='edit_form'),
    path('blog_form/',views.blog_form, name='blog_form'),
    path('add_food/',views.add_food, name='add_food'),
    # path('delete-food/<slug:food_slug>/', views.delete_food, name='delete_food'),
    path('activate/', views.activate, name='activate'),
    path('show_food/', views.show_food, name='show_food'),
    path('show_blog/', views.show_blog, name='show_blog'),
    path('view-blog/<slug:food_slug>', views.view_fooddetails, name='view_fooddetails'),
    path('delete_food/<slug:food_slug>', views.delete_food, name='delete_food'),
    path('delete_user/',views.delete_user, name = 'delete_user'),
    # path('delete_confirm/',TemplateView.as_view(template_nam= "dashboard/delete_cofirm"))
]