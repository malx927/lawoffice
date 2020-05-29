# coding = utf-8
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CompanyContractViewSet, PrivateContractViewSet, PersonInfoViewSet, CompanyInfoViewSet

router = DefaultRouter()
router.register(r'person', PersonInfoViewSet, basename="person")
router.register(r'company', CompanyInfoViewSet, basename="company")
router.register(r'private', PrivateContractViewSet, basename="private")
router.register(r'adviser', CompanyContractViewSet, basename="adviser")

urlpatterns = [
    # path('login/', JSONWebTokenAPIView.as_view(), name="user-api-login"),
]

urlpatterns += router.urls