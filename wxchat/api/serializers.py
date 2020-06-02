# coding = utf-8
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from wxchat.models import SwipeImage


class SwipeImageSerializer(ModelSerializer):
    """
    图片轮播
    """
    class Meta:
        model = SwipeImage
        exclude = ['update_time', 'add_time']

