# coding = utf-8
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from service.models import PersonInfo, CompanyInfo, PrivateContract, CompanyContract, ContractAmount


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


class ContractAmountSerializer(ModelSerializer):
    """合同金额"""
    class Meta:
        model = ContractAmount
        fields = '__all__'


class PrivateContractSerializer(ModelSerializer):
    """
    私人律师信息
    """
    show_code = serializers.SerializerMethodField(read_only=True)
    is_effect = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PrivateContract
        fields = '__all__'

    def get_show_code(self, obj):
        code = obj.code
        if len(code) == 9:
            code_list = code.split("-")
            return '祥私[{}]第{}号'.format(code_list[0], code_list[1])
        else:
            return obj.code

    def get_is_effect(self,obj):
        if obj.is_success:
            return '已生效'
        else:
            return '未生效'


class CompanyContractSerializer(ModelSerializer):
    """
    法律顾问信息
    """
    show_code = serializers.SerializerMethodField(read_only=True)
    is_effect = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CompanyContract
        fields = '__all__'

    def get_show_code(self, obj):
        code = obj.code
        if len(code) == 9:
            code_list = code.split("-")
            return '祥企[{}]第{}号'.format(code_list[0], code_list[1])
        else:
            return obj.code

    def get_is_effect(self, obj):
        if obj.is_success:
            return '已生效'
        else:
            return '未生效'
