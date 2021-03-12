import inspect

from django.apps import AppConfig
from django.utils.module_loading import import_string, import_module


class RbacConfig(AppConfig):
    name = 'APPS.RBAC'

    # def ready(self):
    #     Permissions = import_string("APPS.RBAC.models.Permissions")
    #     permissions = import_module("Module_Auth.Permissions.RBAC_Permissions")
    #     clsmembers = inspect.getmembers(permissions, inspect.isclass)
    #     classes = [(c[0], c[1].__doc__.strip()) for c in clsmembers if
    #                c[0] not in ('MainPermission', 'SecondaryPermission')]
    #     prefixes = [('GET', '获取'), ('PUT', '修改'), ('POST', '创建'), ('DELETE', '删除')]
    #     for prefix in prefixes:
    #         for Permission in classes:
    #             Permissions.objects.get_or_create(name=f"{prefix[1]}{Permission[1]}",
    #                                               codeName=f"{prefix[0]}_{Permission[0]}")
