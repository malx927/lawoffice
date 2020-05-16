from rest_framework.permissions import BasePermission
from wxchat.models import WxUserInfo


class WeixinPermission(BasePermission):

    def has_permission(self, request, view):
        openid = request.query_params.get("openid", None)
        if openid is None:
            return False

        wx_user = WxUserInfo.objects.filter(openid=openid).first()
        if wx_user:
            return True
        else:
            return False
