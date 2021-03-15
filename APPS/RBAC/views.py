from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from APPS.RBAC.models import User
from Module_Auth.Authentications.RBAC_Authentications import UserAuthentication
from Module_Auth.Permissions.RBAC_Permissions import UserPermission, GroupUserPermission
from Module_Custom.Custom_Exception import LoginFailed
from Module_Custom.Custom_Permission import action
from Module_Custom.Custom_Token import make_rbac_token
from Module_Serializers.RBAC_Serializer.RBACUserSerializer import UserSerializer


# TODO LOGIN DEMO ↓
class Login(APIView):
    """
    登录DEMO
    """

    def post(self, request):
        account = request.data.get("account")
        # DEMO使用未加密明文密码
        password = request.data.get("password")
        user = User.objects.filter(account=account, password=password).first()
        if user:
            token = make_rbac_token(user.id)
        else:
            raise LoginFailed

        return Response({
            "code": 200,
            "token": token
        })


# TODO DEMO ↓
class Users(ModelViewSet):
    """
    所有用户
    """

    # 用户认证
    authentication_classes = [UserAuthentication]
    # 一级权限认证 ↓
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 二级权限认证 DEMO_1 ↓
    # permission参数为字符串时 使用默认权限类
    # 生成以 被装饰的类方法名role_user作为codeName值 / permission参数作为name值 的权限表数据
    # 生成权限表数据方式详见 Module_Custom.Custom_Permission.action => DEMO
    # inherit为True 此时继承一级权限结果 UserPermission 认证通过则无需认证role_user权限
    @action(methods=["get"], detail=False, permission="指定角色用户", inherit=True)
    def role_user(self, request):
        """
        某一角色的用户接口
        """
        return Response({
            "code": 200
        })

    # 二级权限认证 DEMO_2 ↓
    # permission参数为自定义二级权限类时
    # 生成权限表数据方式详见 Module_Auth.Permissions.RBAC_Permissions => DEMO
    # inherit为False 此时不继承一级权限 无论一级权限是否通过 必须有group_user权限才能访问此接口
    @action(methods=["get"], detail=False, permission=GroupUserPermission, inherit=False)
    def group_user(self, request):
        """
        某一分组的用户接口
        """
        return Response({
            "code": 200
        })
