from django.contrib import admin
from .models import ShopUser
from django.contrib.auth.admin import UserAdmin
from .forms import ShopUserCreationForm, ShopUserChangeForm

# Register your models here.

@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    add_form = ShopUserCreationForm
    form = ShopUserChangeForm
    model = ShopUser
    list_display = ['phone', 'first_name', 'last_name', 'is_superuser', 'is_active']
    fieldsets =  (
        (None, {'fields' : ('phone', 'password')}),
        ('Personal info', {'fields' : ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields' : ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields' : ('last_login', 'date_joined')}),
        )
    add_fieldsets =  (
        (None, {'fields' : ('phone', 'password')}),
        ('Personal info', {'fields' : ('first_name', 'last_name', 'address')}),
        ('Permissions', {'fields' : ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields' : ('last_login', 'date_joined')}),
        )