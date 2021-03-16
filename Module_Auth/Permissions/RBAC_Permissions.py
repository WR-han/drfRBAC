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
