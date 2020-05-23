# coding = utf-8
from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.api.authentication import authenticate

from office.models import Office


class OfficeSerializer(ModelSerializer):
    """
    律所信息
    """
    class Meta:
        model = Office
        exclude = ['bank', 'account', 'update_time', 'add_time']

