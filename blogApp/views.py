from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Post
from ProjectApp.forms import CommentForm

# Create your views here.
class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog/blog_app.html'
    

# class blogDetail(generic.DetailView):
#     model = Post
#     template_name = 'blog/blog_detail.html'
#     context_object_name = 'blogDetail'

def blogDetail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    template_name = 'blog/blog_detail.html'
    if request.method == 'POST':
        comment_form =CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name,{'post': post,
                                          'comments': comments,
                                           'new_comments': new_comment,
                                           'comment_form': comment_form})

# def comment_detail(request, slug):
#     template_name = 'blog/comment_detail.html'
#     post = get_object_or_404(Post, slug=slug)
#     comments = post.comments.filter(active=True)
#     new_comment = None
#     if request.method == 'POST':
#         comment_form =CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.save()
#     else:
#         comment_form = CommentForm()
#     return render(request, template_name,{'post': post,
#                                           'comments': comments,
#                                            'new_comments': new_comment,
#                                            'comment_form': comment_form})
