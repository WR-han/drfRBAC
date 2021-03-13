"""
权限类分为两种 一级权限类/二级权限类

此处所有权限类在 项目运行初始 会生成Permissions表（model位置 APPS=>RBAC=>models=>Permissions）数据
    数据字段来源：
        name => f"{method对应的请求方式}{当前类的注释内容}"
        codeName => f"{method}_{当前类名}"

* 权限类 必须 写注释用来创建权限数据
* 如无需重写 has_permission 继承后内容可以pass
* 一般情况下 不会 创建二级权限类，可在 action装饰器 中使用默认权限类（详见Module_Custom.Custom_Permission.action）
* 通常以下情况需要创建二级权限类：
    1. 需要重写权限类的 has_permission 方法
    2. 多个接口（action装饰器）需使用同一个二级权限
* 具体查看DEMO
"""
from Module_Custom.Custom_Permission import MainPermission, SecondaryPermission


class UserPermission(MainPermission):
    """
    全部用户信息
    """
    ...
    """
    ↑ DEMO_1
    一级权限 配置于ModelViewSet的permission_classes中
    自动生成Permissions表数据:
        name            codeName
        -------------------------------------
        获取全部用户信息	GET_UserPermission
        修改全部用户信息	PUT_UserPermission
        创建全部用户信息	POST_UserPermission
        删除全部用户信息	DELETE_UserPermission
    """


class GroupUserPermission(SecondaryPermission):
    """
    特定分组下用户信息
    """
    ...
    """
    ↑ DEMO_2
    二级权限 配置于@action装饰器中
    自动生成Permissions表数据:
        name                codeName
        ------------------------------------------------
        获取特定分组下用户信息	GET_IdentityUserPermission
        修改特定分组下用户信息	PUT_IdentityUserPermission
        创建特定分组下用户信息	POST_IdentityUserPermission
        删除特定分组下用户信息	DELETE_IdentityUserPermission
    """
