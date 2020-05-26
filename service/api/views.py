# coding = utf-8
from io import BytesIO

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from wxchat.api.permissions import WeixinPermission

from service.models import PersonInfo, CompanyInfo, PrivateContract, CompanyContract
from wxchat.models import WxUserInfo

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
    permission_classes = (WeixinPermission,)
    pagination_class = None
    queryset = PrivateContract.objects.all()
    serializer_class = PrivateContractSerializer

    def get_queryset(self):
        openid = get_openid_from_header(self.request)
        print(openid, '::::::::::::::::::')
        if openid:
            queryset = super().get_queryset()
            return queryset.filter(Q(openid=openid) | Q(office_openid=openid))
        else:
            return None

    def get_object(self):
        obj = super().get_object()
        print(':::::::::::', obj.name)
        if not obj.is_success:
            openid = get_openid_from_header(self.request)
            print(openid, ':------------')
            if openid:
                user = self.get_user(openid)
                if user:
                    obj.office_openid = openid
                    obj.office_man = user.name
                    obj.office_man_tel = user.telephone
                    obj.save()
        return obj

    def get_user(self, openid):
        if openid is None:
            return None
        user = WxUserInfo.objects.filter(openid=openid, member_role=1).first()  # member_role[ 1为销售]
        return user if user is not None else None


class CompanyContractViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = CompanyContract.objects.all()
    serializer_class = CompanyContractSerializer











