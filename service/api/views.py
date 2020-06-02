# coding = utf-8
from django.db.models import Q

from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from wxchat.api.permissions import WeixinPermission

from service.models import PersonInfo, CompanyInfo, PrivateContract, CompanyContract, ContractAmount
from wxchat.models import WxUserInfo

from .serializers import PersonInfoSerializer, CompanyInfoSerializer, PrivateContractSerializer, \
    CompanyContractSerializer, ContractAmountSerializer
from wxchat.utils import get_openid_from_header


def get_user(openid):
    if openid is None:
        return None
    user = WxUserInfo.objects.filter(openid=openid).first()
    return user


class PersonInfoViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    # permission_classes = (WeixinPermission, )
    pagination_class = None
    queryset = PersonInfo.objects.all()
    serializer_class = PersonInfoSerializer
    lookup_field = 'openid'
    lookup_url_kwarg = 'openid'


class CompanyInfoViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    lookup_field = 'openid'
    lookup_url_kwarg = 'openid'


class ContractAmountViewSet(ReadOnlyModelViewSet):
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = ContractAmount.objects.all()
    serializer_class = ContractAmountSerializer


class PrivateContractViewSet(ModelViewSet):
    authentication_classes = ()
    permission_classes = (WeixinPermission,)
    pagination_class = None
    queryset = PrivateContract.objects.all()
    serializer_class = PrivateContractSerializer

    def get_queryset(self):
        openid = get_openid_from_header(self.request)
        print(openid, '::::::::::::::::::')
        queryset = super().get_queryset()
        if openid:
            user = get_user(openid)
            if user is None:
                return None

            if self.lookup_field in self.kwargs:
                return queryset

            if user and user.is_super == 1:
                return queryset
            else:
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
                user = get_user(openid)
                if user and user.member_role_id == 1:  # 销售人员
                    obj.office_openid = openid
                    obj.office_man = user.name
                    obj.office_man_tel = user.telephone
                    obj.save()
        return obj


class CompanyContractViewSet(ModelViewSet):
    authentication_classes = ()
    permission_classes = (WeixinPermission,)
    pagination_class = None
    queryset = CompanyContract.objects.all()
    serializer_class = CompanyContractSerializer

    def get_queryset(self):
        openid = get_openid_from_header(self.request)
        print(openid, 'CompanyContractViewSet')
        queryset = super().get_queryset()
        if openid:
            user = get_user(openid)
            if user is None:
                return None
            if self.lookup_field in self.kwargs:
                return queryset

            if user and user.is_super == 1:
                return queryset
            else:
                return queryset.filter(Q(openid=openid) | Q(office_openid=openid))
        else:
            return None

    def get_object(self):
        obj = super().get_object()
        if not obj.is_success:
            openid = get_openid_from_header(self.request)
            print(openid, 'CompanyContractViewSet :get_object')
            if openid:
                user = get_user(openid)
                if user and user.member_role_id == 2:      # member_role[ 2 为法律顾问代理]
                    obj.office_openid = openid
                    obj.office_man = user.name
                    obj.office_man_tel = user.telephone
                    obj.save()
        return obj


class CompanyAgencyViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    authentication_classes = ()
    permission_classes = (WeixinPermission,)
    pagination_class = None
    queryset = CompanyInfo.objects.all()
    serializer_class = CompanyInfoSerializer
    lookup_field = 'openid'
    lookup_url_kwarg = 'openid'







