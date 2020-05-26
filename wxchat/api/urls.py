# coding = utf-8
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import QrCodeAPIView

# router = DefaultRouter()
# router.register(r'person', PersonInfoViewSet, basename="person")
#

urlpatterns = [
    path('qrcode/', QrCodeAPIView.as_view(), name="qr-code"),
]
