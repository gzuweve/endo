from django.contrib import admin
from .models import *
from django.contrib import auth
# Register your models here.
# admin.site.register(User)
# admin.site.register(Order)
# admin.site.register(Material)
from main.models import (User, Order, Material)
@admin.register(User)
class UserAdmin(auth.admin.UserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'second_name')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'drawing', 'information')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'material', 'deadline', 'status')

