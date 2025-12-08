# from django.contrib import admin
# from django.contrib.admin.forms import AdminPasswordChangeForm
#
# from .models import *
# from django.contrib import auth
# # Register your models here.
# # admin.site.register(User)
# # admin.site.register(Order)
# # admin.site.register(Material)
# from main.models import (User, Order, Material)
# class PasswordEyeAdminPasswordChangeForm(AdminPasswordChangeForm):
#     class Media:
#         js = ('admin/password_eye.js',)
#
# @admin.register(User)
# class UserAdmin(auth.admin.UserAdmin):
#     #change_password_form =  PasswordEyeAdminPasswordChangeForm
#     list_display = ('username', 'last_name', 'first_name', 'second_name')
#     class Media:
#         js = ("admin/password_eye.js",)
#
# @admin.register(Material)
# class MaterialAdmin(admin.ModelAdmin):
#     list_display = ('name', 'drawing', 'information')
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'material', 'deadline', 'status')

