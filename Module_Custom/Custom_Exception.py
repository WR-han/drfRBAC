from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class WechatValidationFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('无法获取用户openid/unionid')
    default_code = 'wechat_validation_failed'


class LoginFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('找不到用户')
    default_code = 'Incorrect_account_or_password'


class PermissionFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('没有相应权限')
    default_code = 'Insufficient_permissions'
