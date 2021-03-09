"""
权限分为两类 一级权限/二级权限

一级权限：
    继承MainPermission
    只能配置在ModelViewSet => permission_classes中
二级权限：
    继承SecondaryPermission
    只能配置在action装饰器的 permission参数中

此处所有权限类在项目运行初始会在Permissions表（model位置 APPS=>RBAC=>models=>Permissions）中生成对应权限数据
    数据字段：
        name => method对应的请求方式 + 当前类的注释内容
        codeName => method + “_” + 当前类名

* 如无需重写 has_permission 方法 直接继承即可（需写注释用来创建权限数据）
* 一般情况下不会创建二级权限类，可在 action装饰器 中使用默认权限类（详见action装饰器） 特殊情况下会创建二级权限类
    1. 需要重新加工权限类的 has_permission 方法
    2. 多个接口需使用同一权限类
* 具体查看DEMO
"""
from Module_Custom.Custom_Permission import MainPermission, SecondaryPermission

"""
    DEMO_1 UserPermission(MainPermission)
    一级权限 配置于ModelViewSet的permission_classes中
    自动生成Permissions表数据:
        name            codeName
        -------------------------------------
        获取全部用户信息	GET_UserPermission
        修改全部用户信息	PUT_UserPermission
        创建全部用户信息	POST_UserPermission
        删除全部用户信息	DELETE_UserPermission


    DEMO_2 DepartmentPermission(SecondaryPermission)
    二级权限 配置于@action装饰器中
    自动生成Permissions表数据:
        name                codeName
        ------------------------------------------------
        获取特定分组下用户信息	GET_IdentityUserPermission
        修改特定分组下用户信息	PUT_IdentityUserPermission
        创建特定分组下用户信息	POST_IdentityUserPermission
        删除特定分组下用户信息	DELETE_IdentityUserPermission
"""


class UserPermission(MainPermission):
    """
    全部用户信息
    """
    ...


class IdentityUserPermission(SecondaryPermission):
    """
    特定分组下用户信息
    """
    ...
