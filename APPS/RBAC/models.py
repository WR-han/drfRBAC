from django.db import models

from Module_Custom.Custom_Model import BaseModel, AccountModel


class User(AccountModel):
    """
    用户
    """
    identity = models.ManyToManyField("RBAC.Identity", verbose_name="身份", through="RBAC.UserIdentity",
                                      related_name="User")
    Permissions = models.ManyToManyField("RBAC.Permissions", verbose_name="权限", through="RBAC.UserPermissions",
                                         related_name="User")

    @property
    def get_permissions(self):
        """
        获取全部权限
        :return:
        """
        my_permissions = [my_pm.codeName for my_pm in self.Permissions.all()]
        my_identity = self.identity.all()
        identity_permission = []
        for dep in my_identity:
            identity_permission += [dep_pm.codeName for dep_pm in dep.Permissions.all()]
        my_permissions += identity_permission
        return my_permissions

    def __str__(self):
        return f"RBAC_用户_{self.nickName}"

    class Meta:
        db_table = 'drfRBAC_User'
        verbose_name = "1.用户表"
        verbose_name_plural = verbose_name


class Identity(BaseModel):
    """
    身份表（可作为身份类型）
    """

    superior = models.ForeignKey("self", blank=True, default="", on_delete=models.SET_DEFAULT,
                                 related_name="lowerLevel", verbose_name="上级", db_constraint=False)
    Group = models.ForeignKey("RBAC.Group", blank=True, default="", on_delete=models.SET_DEFAULT,
                              related_name="Identity", verbose_name="分组", db_constraint=False)
    Permissions = models.ManyToManyField("RBAC.Permissions", verbose_name="权限",
                                         through="RBAC.IdentityPermissions", related_name="Identity")

    name = models.CharField("身份名称", max_length=15, unique=True)

    def __str__(self):
        return f"RBAC_身份_{self.name}"

    class Meta:
        db_table = 'drfRBAC_Identity'
        verbose_name = "2.身份表"
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


class UserIdentity(BaseModel):
    """
    用户/身份关系表
    """

    User = models.ForeignKey("RBAC.User", on_delete=models.CASCADE, verbose_name="用户",
                             related_name="UserIdentity", db_constraint=False)
    identity = models.ForeignKey("RBAC.Identity", on_delete=models.CASCADE, verbose_name="身份",
                                 related_name="UserIdentity", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.identity.name}_{self.User.nickName}"

    class Meta:
        db_table = 'drfRBAC_User_Identity'
        verbose_name = "5.用户/身份关系表"
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


class IdentityPermissions(BaseModel):
    """
    身份/权限关系表
    """

    identity = models.ForeignKey("RBAC.Identity", on_delete=models.CASCADE, verbose_name="身份",
                                 related_name="IdentityPermissions", db_constraint=False)
    Permissions = models.ForeignKey("RBAC.Permissions", on_delete=models.CASCADE, verbose_name="权限",
                                    related_name="IdentityPermissions", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.identity.name}_{self.Permissions.name}"

    class Meta:
        db_table = 'drfRBAC_identity_permissions'
        verbose_name = "7.身份/权限关系表"
        verbose_name_plural = verbose_name
