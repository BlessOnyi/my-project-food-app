from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

STATUS =(
     (0,"Draft"),
     (1,"Publish")
)
class Post(models.Model):
     title = models.CharField(max_length=300, verbose_name=None, unique=True)
     image = models.ImageField(upload_to='media/')
     slug = models.SlugField(max_length=300, unique=True)
     author = models.ForeignKey(User, on_delete=models.CASCADE)
     updated_on = models.DateTimeField(auto_now = True)
     content = models.TextField()
     created_on = models.DateTimeField(auto_now_add=True)
     status = models.IntegerField(choices=STATUS, default=0)


     class Meta:
          ordering = ['-created_on']

     def __str__(self):
          return self.title


# Create your models here.
