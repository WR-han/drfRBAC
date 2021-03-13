from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from APPS.RBAC.models import User
from Module_Auth.Permissions.RBAC_Permissions import UserPermission, GroupUserPermission
from Module_Custom.Custom_Permission import action
from Module_Serializers.RBAC_Serializer.RBACUserSerializer import UserSerializer


# TODO DEMO ↓
class Users(ModelViewSet):
    """
    所有用户
    """
    # 一级权限认证 ↓
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 二级权限认证 DEMO_1 ↓
    # permission参数为字符串时 使用默认权限类
    # 生成以 被装饰的类方法名identity_user作为codeName值 / permission参数作为name值 的权限表数据
    # 生成权限表数据方式详见 Module_Custom.Custom_Permission.action => DEMO
    # inherit为True 此时继承一级权限结果 UserPermission 认证通过则无需认证identity_user权限
    @action(methods=["get"], detail=False, permission="指定身份用户", inherit=True)
    def identity_user(self, request):
        """
        指定身份用户接口
        """
        print(request.user)
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
        指定身份用户接口
        """
        print(request.user)
        return Response({
            "code": 200
        })
