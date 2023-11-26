from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.urls import reverse

# Create your models here.



# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return super(ProductManager, self).get_queryset().filter(is_active=True)
    

class Category(models.Model):
    name = models.CharField(max_length = 200, null= False)
    slug = models.SlugField(max_length= 200, unique = True)


    class Meta:
        verbose_name_plural ='categories'

    
    def __str__(self):
        return self.name
    
class Products(models.Model):
    category = models.ForeignKey(Category, related_name='product',on_delete =models.CASCADE)
    created_by =models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length =200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=200)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    

    
    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created_on',)

    def get_absolute_url(self):
        return reverse('ProjectApp:product_detail', args=[self.slug])

    
    def __str__(self):
        return self.title

# Create your models here.
