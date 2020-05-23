# coding = utf-8
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from wxchat.api.permissions import WeixinPermission

from office.models import Office
from .serializers import OfficeSerializer


class OfficeViewSet(ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = ()
    pagination_class = None
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer









