# coding = utf-8
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.api.authentication import authenticate

from service.models import PersonInfo, CompanyInfo, PrivateContract, CompanyContract


class PersonInfoSerializer(ModelSerializer):
    """
    客户信息
    """
    class Meta:
        model = PersonInfo
        exclude = ['update_time', 'add_time']


class CompanyInfoSerializer(ModelSerializer):
    """
    公司信息
    """
    class Meta:
        model = CompanyInfo
        exclude = ['update_time', 'add_time']


class PrivateContractSerializer(ModelSerializer):
    """
    私人律师信息
    """

    class Meta:
        model = PrivateContract
        fields = '__all__'


class CompanyContractSerializer(ModelSerializer):
    """
    法律顾问信息
    """

    class Meta:
        model = CompanyContract
        fields = '__all__'

