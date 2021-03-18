from django.db import models

from Module_Custom.Custom_Model import BaseModel, AccountModel


class User(AccountModel):
    """
    用户
    """
    Role = models.ManyToManyField("RBAC.Role", verbose_name="角色", through="RBAC.UserRole",
                                  related_name="User")
    Permissions = models.ManyToManyField("RBAC.Permissions", verbose_name="权限", through="RBAC.UserPermissions",
                                         related_name="User")

    @property
    def get_permissions(self):
        """
        获取全部权限
        :return:
        """
        # print(self.UserPermissions.filter(isValid=1))
        self_permissions = [self_pm.Permissions.codeName for self_pm in self.UserPermissions.filter(isValid=1)]
        self_role = [self_r.Role for self_r in self.UserRole.filter(isValid=1)]
        role_permission = []
        for dep in self_role:
            role_permission += [dep_pm.Permissions.codeName for dep_pm in dep.RolePermissions.filter(isValid=1)]
        self_permissions += role_permission
        return self_permissions

    def __str__(self):
        return f"RBAC_用户_{self.nickName}"

    class Meta:
        db_table = 'drfRBAC_User'
        verbose_name = "1.用户表"
        verbose_name_plural = verbose_name


class Role(BaseModel):
    """
    角色表（可作为岗位类型）
    """

    superior = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name="lowerLevel", verbose_name="上级", db_constraint=False)
    Group = models.ForeignKey("RBAC.Group", blank=True, null=True, on_delete=models.SET_NULL,
                              related_name="Role", verbose_name="分组", db_constraint=False)
    Permissions = models.ManyToManyField("RBAC.Permissions", verbose_name="权限",
                                         through="RBAC.RolePermissions", related_name="Role")

    name = models.CharField("角色名称", max_length=15, unique=True)

    def __str__(self):
        return f"RBAC_角色_{self.name}"

    class Meta:
        db_table = 'drfRBAC_Role'
        verbose_name = "2.角色表"
        verbose_name_plural = verbose_name


class Group(BaseModel):
    """
    分组表（可作为部门）
    """

    name = models.CharField("分组名称", max_length=15, unique=True)

    def __str__(self):
        return f"RBAC_分组_{self.name}"

    class Meta:
        db_table = 'drfRBAC_Group'
        verbose_name = "3.分组表"
        verbose_name_plural = verbose_name


class Permissions(BaseModel):
    """
    权限表
    """

    name = models.CharField("权限名称", max_length=15)
    codeName = models.CharField("权限代码", max_length=30)

    def __str__(self):
        return f"RBAC_权限_{self.name}"

    class Meta:
        db_table = 'drfRBAC_Permissions'
        verbose_name = "4.权限表"
        verbose_name_plural = verbose_name


class UserRole(BaseModel):
    """
    用户/角色关系表
    """

    User = models.ForeignKey("RBAC.User", on_delete=models.CASCADE, verbose_name="用户",
                             related_name="UserRole", db_constraint=False)
    Role = models.ForeignKey("RBAC.Role", on_delete=models.CASCADE, verbose_name="角色",
                             related_name="UserRole", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.Role.name}_{self.User.nickName}"

    class Meta:
        db_table = 'drfRBAC_User_Role'
        verbose_name = "5.用户/角色关系表"
        verbose_name_plural = verbose_name


class UserPermissions(BaseModel):
    """
    用户/权限关系表
    """

    User = models.ForeignKey("RBAC.User", on_delete=models.CASCADE, verbose_name="用户",
                             related_name="UserPermissions", db_constraint=False)
    Permissions = models.ForeignKey("RBAC.Permissions", on_delete=models.CASCADE, verbose_name="权限",
                                    related_name="UserPermissions", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.User.nickName}_{self.Permissions.name}"

    class Meta:
        db_table = 'drfRBAC_User_Permissions'
        verbose_name = "6.用户/权限关系表"
        verbose_name_plural = verbose_name


class RolePermissions(BaseModel):
    """
    角色/权限关系表
    """

    Role = models.ForeignKey("RBAC.Role", on_delete=models.CASCADE, verbose_name="角色",
                             related_name="RolePermissions", db_constraint=False)
    Permissions = models.ForeignKey("RBAC.Permissions", on_delete=models.CASCADE, verbose_name="权限",
                                    related_name="RolePermissions", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.Role.name}_{self.Permissions.name}"

    class Meta:
        db_table = 'drfRBAC_role_permissions'
        verbose_name = "7.角色/权限关系表"
        verbose_name_plural = verbose_name
