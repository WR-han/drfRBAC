import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from APP_RBAC.models import User
from Module_Public.key import RBAC_token_salt


class RBACAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        try:
            res = jwt.decode(token.encode(), RBAC_token_salt, algorithms='HS256')
            user_id = res.get("id")
            user_obj = User.objects.get(id=user_id)
            return user_obj, token
        except jwt.exceptions.DecodeError:
            raise AuthenticationFailed("无效token")
        except jwt.exceptions.ExpiredSignatureError:
            raise AuthenticationFailed("token超时")
        except Exception as e:
            raise AuthenticationFailed(e)

