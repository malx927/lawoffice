# coding = utf-8
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.api.utils import jwt_response_payload_handler

from users.models import UserInfo, Role, Permission
from .serializers import UserInfoSerializer, RoleSerializer, PermissionSerializer, PermissionListSerializer, \
    JSONWebTokenSerializer


class JSONWebTokenAPIView(APIView):
    """
    JWT API View .
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        serializer = JSONWebTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token = serializer.validated_data["token"]
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfoViewSet(ModelViewSet):
    # permission_classes = ()
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer


class RoleViewSet(ModelViewSet):
    permission_classes = ()
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class PermissionViewSet(ModelViewSet):
    permission_classes = ()
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionListViewSet(ReadOnlyModelViewSet):
    permission_classes = ()
    pagination_class = ()
    queryset = Permission.objects.filter(parent__isnull=True)
    serializer_class = PermissionListSerializer






