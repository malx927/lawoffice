# coding = utf-8
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import QrCodeAPIView, SwipeImageViewSet, UserRoleViewSet

router = DefaultRouter()
router.register(r'swipe', SwipeImageViewSet, basename="swipe")
router.register(r'role', UserRoleViewSet, basename="role")

urlpatterns = [
    path('qrcode/', QrCodeAPIView.as_view(), name="qr-code"),
]

urlpatterns += router.urls