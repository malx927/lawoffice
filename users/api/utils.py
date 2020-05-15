import datetime
import jwt
from django.conf import settings

JWT_ALGORITHM = 'HS256'


def jwt_payload_handler(user):
    if user is None:
        return None

    payload = {
        'user_id': user.pk,
        'username': user.name,
        'exp': datetime.datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
        'iat': datetime.datetime.utcnow(),  # 开始时间
    }

    if settings.JWT_AUDIENCE is not None:
        payload['aud'] = settings.JWT_AUDIENCE

    if settings.JWT_ISSUER is not None:
        payload['iss'] = settings.JWT_ISSUER

    return payload


def jwt_encode_handler(payload):
    key = settings.SECRET_KEY
    return jwt.encode(payload, key, JWT_ALGORITHM).decode('utf-8')


def jwt_decode_handler(token):
        options = {
            'verify_exp': settings.JWT_VERIFY_EXPIRATION,
        }
        secret_key = settings.SECRET_KEY
        return jwt.decode(
            token,
            secret_key,
            True,
            options=options,
            audience=settings.JWT_AUDIENCE,
            issuer=settings.JWT_ISSUER,
            algorithms=[JWT_ALGORITHM]
        )


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {
        'token': token
    }


def jwt_get_username_from_payload(payload):
    """
    Override this function if username is formatted differently in payload
    """
    return payload.get('username')
