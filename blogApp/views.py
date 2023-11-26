from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/blog_app.html'
    

class blogDetail(generic.DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blogDetail'
    
