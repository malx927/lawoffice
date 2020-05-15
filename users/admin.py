from django.contrib import admin
from .models import UserInfo, Role, Permission, Post


@admin.register(Post)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'real_name', 'gender', 'telephone', 'is_superuser', 'is_active']


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'path', 'level', 'parent', 'sort']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'only_own']



