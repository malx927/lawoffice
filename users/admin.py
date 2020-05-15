from django.contrib import admin
from django.contrib.admin import register

from .models import UserInfo, Role, Permission


@register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'real_name', 'gender', 'telephone', 'is_superuser', 'is_active']


@register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'path', 'level', 'parent', 'sort']


@register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'only_own']
