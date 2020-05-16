# coding = utf-8
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from wxchat.api.permissions import WeixinPermission

from service.models import PersonInfo, CompanyInfo, PrivateContract, CompanyContract
from .serializers import PersonInfoSerializer, CompanyInfoSerializer, PrivateContractSerializer, CompanyContractSerializer


class PersonInfoViewSet(ModelViewSet):
    authentication_classes = ()
    # permission_classes = (WeixinPermission, )
    pagination_class = None
    queryset = PersonInfo.objects.all()
    serializer_class = PersonInfoSerializer


class CompanyInfoViewSet(ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer


class PrivateContractViewSet(ModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = PrivateContract.objects.all()
    serializer_class = PrivateContractSerializer


class CompanyContractViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = CompanyContract.objects.all()
    serializer_class = CompanyContractSerializer






