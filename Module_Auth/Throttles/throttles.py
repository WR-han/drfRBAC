from rest_framework.exceptions import NotAuthenticated
from rest_framework.throttling import SimpleRateThrottle


class BaseThrottle(SimpleRateThrottle):
    scope = 'base'

    def get_cache_key(self, request, view):
        if request.user:
            ident = request.user.pk
        else:
            raise NotAuthenticated("无法获取您的账号相关信息，请确认已经登陆")

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
