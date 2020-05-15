# coding = utf-8
import jwt
from django.utils.encoding import smart_text
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from django.conf import settings
from users.api.utils import jwt_decode_handler, jwt_get_username_from_payload
from users.models import UserInfo


def authenticate(**credentials):
    username = credentials.get("username", None)
    password = credentials.get("password", None)
    print(username, password)
    if username is None or password is None:
        return None

    user = UserInfo.objects.filter(name=username, is_active=True).first()

    if user is None:
        return None

    if user.check_password(password):
        return user
    else:
        return None


class JSONWebTokenAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """
    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        token = self.get_token_value(request)
        print("JSONWebTokenAuthentication::authenticate", token)
        if token is None:
            msg = {
                'status_code': 401,
                'message': '没有token,请重新登录'
            }
            raise exceptions.AuthenticationFailed(msg)

        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            msg = {
                'status_code': 401,
                'message': 'token 已经过期'
            }
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = {
                'status_code': 401,
                'message': 'token 解码错误'
            }
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            msg = {
                'status_code': 401,
                'message': '无效token 错误'
            }
            raise exceptions.AuthenticationFailed(msg)

        user = self.authenticate_credentials(payload)

        return (user, token)

    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id.
        """
        username = jwt_get_username_from_payload(payload)

        if not username:
            msg = '非法的负载内容'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = UserInfo.objects.get(name=username)
        except UserInfo.DoesNotExist:
            msg = 'token 非法'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = '用户账号已被禁用'
            raise exceptions.AuthenticationFailed(msg)

        return user

    def get_token_value(self, request):
        auth = get_authorization_header(request).split()
        print(auth)
        auth_header_prefix = settings.JWT_AUTH_HEADER_PREFIX.lower()

        if not auth:
            msg = {
                'status_code': 401,
                'message': '没有token,请登录'
            }
            raise exceptions.AuthenticationFailed(msg)

        if auth[0].lower().decode() != auth_header_prefix:
            msg = {
                'status_code': 401,
                'message': 'Authorization格式错误!'
            }
            raise exceptions.AuthenticationFailed(msg)

        if len(auth) == 1:
            msg = {
                'status_code': 401,
                'message': '非法的 Authorization 头. 认证信息不全!'
            }
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = {
                'status_code': 401,
                'message': '非法的 Authorization 头. 认证信息存在多余字符.'
            }
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]



