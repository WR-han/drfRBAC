import inspect
import os

from django.apps import AppConfig
from django.utils.module_loading import import_string, import_module

from drfRBAC.settings import BASE_DIR


class RbacConfig(AppConfig):
    name = 'APPS.RBAC'

    def ready(self):
        try:
            permissions_model = import_string("APPS.RBAC.models.Permissions")
            permissions_model.objects.get_or_create(name="管理员权限", codeName="AdminPermission")
            permissions_dir = os.listdir(os.path.join(BASE_DIR, "Module_Auth", "Permissions"))
            for permission_py in permissions_dir:
                if ".py" in permission_py:
                    permission_name = permission_py.split(".py")[0]
                    permissions = import_module(f"Module_Auth.Permissions.{permission_name}")
                    class_members = inspect.getmembers(permissions, inspect.isclass)
                    print(class_members)
                    classes = [(c[0], c[1].__doc__.strip()) for c in class_members if
                               c[0] not in ('MainPermission', 'SecondaryPermission')]
                    prefixes = [('GET', '获取'), ('PUT', '修改'), ('POST', '创建'), ('DELETE', '删除')]
                    for prefix in prefixes:
                        for Permission in classes:
                            permissions_model.objects.get_or_create(name=f"{prefix[1]}{Permission[1]}",
                                                                    codeName=f"{prefix[0]}_{Permission[0]}")
                            print(f"<{prefix[1]}{Permission[1]}> 权限创建成功")
                    print(f"---------------{permission_py} 模块内权限数据创建/检查完毕")
        except Exception as e:
            print(f"权限数据未创建，请先进行migrate操作,{e}")
