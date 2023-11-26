from . import views
from django.urls import path

app_name =  'blogApp'
urlpatterns =[
    path('', views.PostList.as_view(), name = 'blogApp'),
    path('blogDetail/<slug:slug>', views.blogDetail.as_view(), name='blog_detail'),
]