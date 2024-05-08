from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from . models import *
# Register your models here.
# admin.site.site_header =

 
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price','slug', 'in_stock', 'created_on', 'updated_on')
    list_filter = ('in_stock', 'is_active')
    list_editable = ('price', 'in_stock')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Products,ProductAdmin)



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_vendor', 'is_user', 'is_active')
    list_filter = ('is_vendor', 'is_user', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'gender')}),
        ('Permissions', {'fields': ('is_vendor', 'is_user', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_vendor', 'is_user', 'is_active'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
