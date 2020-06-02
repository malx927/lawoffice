# coding = utf-8
from io import BytesIO

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from wxchat.api.serializers import SwipeImageSerializer
from wxchat.models import SwipeImage
from wxchat.utils import create_qrcode


class QrCodeAPIView(APIView):
    """二维码"""
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        direct_url = request.query_params.get("url")
        f = BytesIO()
        if direct_url:
            image = create_qrcode(direct_url)
            image.save(f, "PNG")

        return HttpResponse(f.getvalue(), content_type="image/png")


class SwipeImageViewSet(ReadOnlyModelViewSet):
    """图片轮播"""
    authentication_classes = ()
    permission_classes = ()
    pagination_class = None
    queryset = SwipeImage.objects.filter(is_show=True)
    serializer_class = SwipeImageSerializer

