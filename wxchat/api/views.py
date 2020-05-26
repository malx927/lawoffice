# coding = utf-8
from io import BytesIO

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from wxchat.utils import create_qrcode


class QrCodeAPIView(APIView):
    """二维码"""
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        direct_url = request.query_params.get("url")
        f = BytesIO()
        if direct_url:
            image = create_qrcode(direct_url)
            print(image)
            image.save(f, "PNG")

        return HttpResponse(f.getvalue(), content_type="image/png")