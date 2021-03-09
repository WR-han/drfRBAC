"""
权限分为两类 一级权限/二级权限

一级权限：
    继承MainPermission
    只能配置在ModelViewSet => permission_classes中
二级权限：
    继承SecondaryPermission
    只能配置在action装饰器的 permission参数中

此处所有权限类在项目运行初始会在
"""
from Module_Public.custom_Permission import MainPermission, SecondaryPermission


class UserPermission(MainPermission):
    """
    全部学生信息
    """
    pass


class DepartmentPermission(SecondaryPermission):
    """
    所在部门旗下学生信息
    """
    pass
