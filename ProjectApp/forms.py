from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django import forms
from django.core import validators
from blogApp.models import *
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from ProjectApp.models import Products



class RegForm(forms.ModelForm):
    user_name = forms.CharField(label='Username :', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Lastname'}))
    email = forms.EmailField(label='Email :',  widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, label='User Type',
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=CustomUser.GENDER_OPTIONS, label='Gender',
                                widget=forms.Select(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'user_name', 'first_name', 'last_name', 'phone_number', 'gender', 'is_vendor', 'is_user')

    # def clean_email(self):
    #     email_field = self.cleaned_data.get('email')
    #     if CustomUser.objects.filter(email=email_field).exists():
    #         raise forms.ValidationError('Email already exist')
    #     return email_field
    
    def clean_password2(self):
        # Check if the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_vendor = self.cleaned_data.get("user_type") == 'vendor'
        user.is_user = self.cleaned_data.get("user_type") == 'user'
        if commit:
            user.save()
        return user






class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))
    new_password2= forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class':'form-control', 'placeholder':'Enter Password'}))

    botfield = forms.CharField(required=False, widget=forms.HiddenInput(),
                               validators=[validators.MaxLengthValidator(0)])

    class Meta():
        model = CustomUser
        fields = ['password1', 'password2']

       

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']
        
        if commit:
            user.save()
            return user
        


class EditUserForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class':'form-control', 'placeholder': 'Enter Username' }))

    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Firstname'}))

    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Lastname'}))
    
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))
   

    botfield = forms.CharField(required=False, widget=forms.HiddenInput(),
                               validators=[validators.MaxLengthValidator(0)])

    class Meta():
        model = User
        fields = ['username',  'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        
        if commit:
            user.save()
            return user
        



class BlogForm(forms.ModelForm):


    class Meta():
        exclude = ['user', 'created_on', 'updated_on']
        model = Post

        widgets={
            'blog_title': forms.TextInput(attrs={'class': 'form-control'}),
            'blog_content' : forms.Textarea(attrs={'class': 'form-control'}),
            'blog_image': forms.FileInput(attrs={'class': 'form-control'}),
           

        }

# class FoodForm(forms.ModelForm):
#     class Meta():
#         exclude = ['user', 'created_on', 'updated_on']
#         model = Products

#         widgets={
#             'food_title': forms.TextInput(attrs={'class': 'form-control'}),
#             'food_price' : forms.DecimalField(attrs={'class': 'form-control'}),
#             'food_image': forms.FileInput(attrs={'class': 'form-control'}),
           

#         }




class FoodForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude = ['created_by', 'created_on', 'updated_on', 'slug', 'is_active', 'description']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Food Title'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file mt-2', 'accept': 'image/*'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price'}),
            'in_stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

        labels = {
            'category': 'Category',
            'title': 'Food Title',
            'image': 'Food Image',
            'price': 'Price',
            'in_stock': 'In Stock',
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name','email','body')
