# coding = utf-8
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OfficeViewSet

router = DefaultRouter()
router.register(r'office', OfficeViewSet, basename="office")


urlpatterns = [
    # path('login/', JSONWebTokenAPIView.as_view(), name="user-api-login"),
]

urlpatterns += router.urls