from django.db import models
from django.contrib.auth.models import User 
from ProjectApp.models import *


# Create your models here.

STATUS =(
     (0,"Draft"),
     (1,"Publish")
)
class Post(models.Model):
     title = models.CharField(max_length=300, verbose_name=None, unique=True)
     image = models.ImageField(upload_to='media/')
     slug = models.SlugField(max_length=300, unique=True)
     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     updated_on = models.DateTimeField(auto_now = True)
     content = models.TextField()
     created_on = models.DateTimeField(auto_now_add=True)
     status = models.IntegerField(choices=STATUS, default=0)


     class Meta:
          ordering = ['-created_on']

     def __str__(self):
          return self.title


# Create your models here.


class Comment(models.Model):
     post = models.ForeignKey(Post,on_delete= models.CASCADE,related_name='comments')
     name= models.CharField(max_length=100)
     email = models.EmailField()
     body = models.TextField()
     created_on= models.DateTimeField(auto_now_add=True)
     active = models.BooleanField(default=False)

     class Meta:
          ordering = ['created_on']

     def __str__(self):
          return 'Comment {} by {}'.format(self.body, self.name)
