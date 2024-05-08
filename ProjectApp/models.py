from django.db import models
from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class CustomAccountManager(BaseUserManager):
    def create_user(self, email, user_name, password, **other_fields):
        if not email:
            raise ValueError("You must provide a valid address")
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, user_name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, user_name, password, **other_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
    ('vendor', 'Vendor'),
    ('user', 'User'),
)

    MALE ='Male'
    FEMALE ='female'
    CHOOSE = ''

    GENDER_OPTIONS =[
        (MALE, 'Male'),
        (FEMALE, 'female'),
        (CHOOSE,  'Select Gender')
    ]


    user_name = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    is_vendor = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    phone_number = models.CharField(max_length = 11)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=30, choices=GENDER_OPTIONS, default=CHOOSE, blank=True, null=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name']

    def _str_(self):
        return self.email


    

class Category(models.Model):
    name = models.CharField(max_length = 200, null= False)
    slug = models.SlugField(max_length= 200, unique = True)


    class Meta:
        verbose_name_plural ='categories'



    
    def __str__(self):
        return self.name
    
class Products(models.Model):
    category = models.ForeignKey(Category, related_name='product',on_delete =models.CASCADE)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='product_creator')
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


