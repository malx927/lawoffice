# coding = utf-8
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.api.authentication import authenticate
from users.api.utils import jwt_payload_handler, jwt_encode_handler

from users.models import UserInfo, Role, Permission


class JSONWebTokenSerializer(Serializer):
    """
    JWT 信息
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # credentials = data.values()
        if all(data):
            user = authenticate(**data)

            if user:
                payload = jwt_payload_handler(user)
                print(payload)
                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = '用户或密码错误,登录失败!'
                raise serializers.ValidationError(msg)
        else:
            msg = '校验错误,必须包括用户和密码'
            raise serializers.ValidationError(msg)


class UserInfoSerializer(ModelSerializer):
    """
    用户信息
    """
    class Meta:
        model = UserInfo
        exclude = ['roles']


class RoleSerializer(ModelSerializer):
    """
    角色信息
    """
    class Meta:
        model = Role
        exclude = ['permissions']


class PermissionSerializer(ModelSerializer):
    """
    权限信息
    """

    class Meta:
        model = Permission
        fields = '__all__'
        # depth = 1


class PermissionListSerializer(ModelSerializer):
    """
    权限信息
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ['id', 'name', 'path', 'level', 'parent', 'children']

    def get_children(self, obj):
        return PermissionListSerializer(obj.perms.all(), many=True).data
