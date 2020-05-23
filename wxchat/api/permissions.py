from rest_framework.permissions import BasePermission
from wxchat.models import WxUserInfo
from wxchat.utils import get_openid_from_header


class WeixinPermission(BasePermission):

    def has_permission(self, request, view):
        # openid = request.query_params.get("openid", None)
        openid = get_openid_from_header(request)
        print("WeixinPermission:", openid)
        if openid is None:
            return False

        wx_user = WxUserInfo.objects.filter(openid=openid).first()
        if wx_user:
            return True
        else:
            return False
