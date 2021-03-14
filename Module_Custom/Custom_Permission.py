from functools import wraps

from django.forms.utils import pretty_name
from rest_framework.decorators import MethodMapper
from rest_framework.permissions import BasePermission, BasePermissionMetaclass

from APPS.RBAC.models import Permissions
from Module_Custom.Custom_Exception import PermissionFailed


class SecondaryPermission(BasePermission):
    """
    所有继承 SecondaryPermission类 的权限类皆为二级权限类
    二级权限类只能配置在 action (当前页line57) 装饰器的 permission参数中
    """

    def has_permission(self, request, view):

        user_permissions = request.user.get_permissions

        if "AdminPermission" in user_permissions:
            return True

        method = request.method
        if request.method == "PATCH":
            method = "PUT"
        need_permission = f"{method}_{type(self).__name__}"

        if need_permission in user_permissions:
            return True
        else:
            return False


class MainPermission(SecondaryPermission):
    """
    所有继承 MainPermission类 的权限类皆为一级权限类
    只能配置在 ModelViewSet => permission_classes 中
    """

    def has_permission(self, request, view):
        base_action = ["list", "retrieve", "create", "update", "partial_update", "destroy"]
        is_check = super(MainPermission, self).has_permission(request, view)
        _action = view.action

        if _action not in base_action:
            # 动作类型不是基础action / 子路由
            if is_check:
                # 拥有主路由权限
                request.main_permission = True

            return True
        else:
            return is_check


def action(methods=None, detail=None, url_path=None, url_name=None, permission=None, inherit=True, **wra_kwargs):
    """
    :param permission: class/str
        class: 自定义的二级权限类
        str: 使用通用权限类时自动生成的权限名称（对应Permission表中的name字段）

        permission为str时  e.g.:
            @action(methods=["get"], detail=False, permission="部分用户")
            def PartUser(self, request):
                ...

        自动生成Permissions表数据:
            name            codeName
            -------------------------------
            获取部分用户	    GET_PartUser
            修改部分用户	    PUT_PartUser
            创建部分用户	    POST_PartUser
            删除部分用户	    DELETE_PartUser

    :param inherit: bool
        是否继承一级权限（permission_classes中的权限类）的认证结果
        值为True（默认）
            一级权限通过 则无需验证二级权限
            一级权限未通过 再验证二级权限
        值为False
            无论一级权限通过与否 必须验证二级权限

    :param methods: 参见源码
    :param detail: 参见源码
    :param url_path: 参见源码
    :param url_name: 参见源码
    """
    methods = ['get'] if (methods is None) else methods
    methods = [method.lower() for method in methods]
    assert detail is not None, (
        "@action() missing required argument: 'detail'"
    )
    if 'name' in wra_kwargs and 'suffix' in wra_kwargs:
        raise TypeError("`name` and `suffix` are mutually exclusive arguments.")

    def wrapper(func):
        func.mapping = MethodMapper(func, methods)
        func.detail = detail
        func.url_path = url_path if url_path else func.__name__
        func.url_name = url_name if url_name else func.__name__.replace('_', '-')
        func.kwargs = wra_kwargs
        if 'name' not in wra_kwargs and 'suffix' not in wra_kwargs:
            func.kwargs['name'] = pretty_name(func.__name__)
        func.kwargs['description'] = func.__doc__ or None

        # 判断是否需要权限（是否生成通用权限）
        if isinstance(permission, str):
            # permission 为字符串时 自动生成通用二级权限类，并且自动生成name为permission参数的Permission表数据
            class GeneralPermission(SecondaryPermission):
                # 创建一个通用二级权限
                ...

            # 修改当前通用二级权限的__name__ 供检查权限时使用
            GeneralPermission.__name__ = func.__name__

            # 创建Permission表数据
            prefixes = [('GET', '获取'), ('PUT', '修改'), ('POST', '创建'), ('DELETE', '删除')]
            try:
                for prefix in prefixes:
                    Permissions.objects.get_or_create(name=f"{prefix[1]}{permission}",
                                                      codeName=f"{prefix[0]}_{GeneralPermission.__name__}")
                    print(f"<{prefix[1]}{permission}> 权限创建成功")
            except Exception as e:
                print(f"权限数据未创建，请先进行migrate操作,{e}")

        @wraps(func)
        def decorated(*args, **kwargs):
            # 权限检查
            view, request = args
            # 是否进行了一级权限验证 True/False为经过检测 None为一级无需检测
            main_permission = getattr(request, "main_permission", None)

            # permission参数 分 3种 None str 自定义permission类
            if isinstance(permission, str):
                # 需要权限（使用通用二级权限类）
                check = GeneralPermission().has_permission(view=view, request=request)

                if inherit and main_permission:
                    # 允许继承一级权限 且 检查通过拥有一级权限
                    return func(*args, **kwargs)
                elif check:
                    # 不允许继承一级权限 或者 没有一级权限 判断是否有当前的二级权限
                    return func(*args, **kwargs)
                else:
                    raise PermissionFailed
            elif isinstance(permission, BasePermissionMetaclass):
                # 需要权限（有指定的自定义二级权限类）
                check = permission().has_permission(view=view, request=request)

                if inherit and main_permission:
                    # 允许继承一级权限 且 拥有一级权限
                    return func(*args, **kwargs)
                elif check:
                    # 不允许继承一级权限 或者 没有一级权限 判断是否有当前的二级权限
                    return func(*args, **kwargs)
                else:
                    raise PermissionFailed
            elif (main_permission is True) or (main_permission is None):
                # 1. 有一级权限且通过并且没有二级权限
                # 2. 没有一级权限（一级权限为None）并且没有二级权限
                return func(*args, **kwargs)
            else:
                raise PermissionFailed

        return decorated

    return wrapper
