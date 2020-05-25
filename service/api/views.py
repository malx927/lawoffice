# coding = utf-8
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from wxchat.api.permissions import WeixinPermission

from service.models import PersonInfo, CompanyInfo, PrivateContract, CompanyContract
from .serializers import PersonInfoSerializer, CompanyInfoSerializer, PrivateContractSerializer, CompanyContractSerializer
from wxchat.utils import get_openid_from_header


class PersonInfoViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    # permission_classes = (WeixinPermission, )
    pagination_class = None
    queryset = PersonInfo.objects.all()
    serializer_class = PersonInfoSerializer
    lookup_field = 'openid'
    lookup_url_kwarg = 'openid'

#
# class CompanyInfoViewSet(ModelViewSet):
#     authentication_classes = ()
#     permission_classes = ()
#     pagination_class = None
#     queryset = CompanyInfo.objects.all()
#     serializer_class = CompanyInfoSerializer


class PrivateContractViewSet(ModelViewSet):
    authentication_classes = ()
    # permission_classes = (WeixinPermission,)
    pagination_class = None
    queryset = PrivateContract.objects.all()
    serializer_class = PrivateContractSerializer

    def get_queryset(self):
        openid = get_openid_from_header(self.request)
        print(openid, '::::::::::::::::::')
        if openid:
            queryset = super().get_queryset()
            return queryset.filter(openid=openid)
        else:
            return None


class CompanyContractViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = CompanyContract.objects.all()
    serializer_class = CompanyContractSerializer






