# coding = utf-8
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserInfoViewSet, RoleViewSet, PermissionViewSet, PermissionListViewSet, JSONWebTokenAPIView

router = DefaultRouter()
router.register(r'user', UserInfoViewSet, basename="users")
router.register(r'role', RoleViewSet, basename="roles")
router.register(r'perm', PermissionViewSet, basename="perms")
router.register(r'permission', PermissionListViewSet, basename="permissions")

urlpatterns = [
    path('login/', JSONWebTokenAPIView.as_view(), name="user-api-login"),
]

urlpatterns += router.urls