from django.db import models

from Module_Custom.Custom_Model import BaseModel, AccountModel


class RBACUser(AccountModel):
    """
    员工账户
    """
    superior = models.ForeignKey("self", blank=True, default="", on_delete=models.SET_DEFAULT,
                                 related_name="lowerLevel", verbose_name="上级负责人", db_constraint=False)
    identity = models.ManyToManyField("RBAC.Identity", verbose_name="所属部门",
                                      through="RBAC.RBACUserIdentity", related_name="RBACUser")
    Permissions = models.ManyToManyField("RBAC.Permissions", verbose_name="权限",
                                         through="RBAC.RBACUserPermissions", related_name="RBACUser")

    @property
    def get_permissions(self):
        my_permissions = [my_pm.codeName for my_pm in self.Permissions.all()]
        my_identity = self.identity.all()
        identity_permission = []
        for dep in my_identity:
            identity_permission += [dep_pm.codeName for dep_pm in dep.Permissions.all()]
        my_permissions += identity_permission
        return my_permissions

    def __str__(self):
        return f"RBAC_员工_{self.nickName}"

    class Meta:
        db_table = 'CSOOA_RBAC_RBACUser'
        verbose_name = "1.员工账户表"
        verbose_name_plural = verbose_name


class Identity(BaseModel):
    """
    岗位表
    """

    superior = models.ForeignKey("self", blank=True, default="", on_delete=models.SET_DEFAULT,
                                 related_name="lowerLevel", verbose_name="上级", db_constraint=False)
    Department = models.ForeignKey("RBAC.Department", blank=True, default="", on_delete=models.SET_DEFAULT,
                                   related_name="Identity", verbose_name="部门", db_constraint=False)
    Permissions = models.ManyToManyField("RBAC.Permissions", verbose_name="权限",
                                         through="RBAC.IdentityPermissions", related_name="Identity")

    name = models.CharField("岗位名称", max_length=15, unique=True)

    def __str__(self):
        return f"RBAC_岗位_{self.name}"

    class Meta:
        db_table = 'CSOOA_RBAC_Identity'
        verbose_name = "2.岗位表"
        verbose_name_plural = verbose_name


class Department(BaseModel):
    """
    部门表
    """

    classifyChoices = ((1, "业务部门"), (2, "行政部门"))

    name = models.CharField("部门名称", max_length=15, unique=True)
    classify = models.BooleanField("部门类型", choices=classifyChoices, default=1)

    def __str__(self):
        return f"RBAC_部门_{self.name}"

    class Meta:
        db_table = 'CSOOA_RBAC_Identity'
        verbose_name = "3.部门表"
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
        db_table = 'CSOOA_RBAC_Permissions'
        verbose_name = "4.权限表"
        verbose_name_plural = verbose_name


class RBACUserIdentity(BaseModel):
    """
    员工/岗位关系表
    """

    RBACUser = models.ForeignKey("RBAC.RBACUser", on_delete=models.CASCADE, verbose_name="员工",
                                 related_name="RBACUserIdentity", db_constraint=False)
    identity = models.ForeignKey("RBAC.Identity", on_delete=models.CASCADE, verbose_name="岗位",
                                 related_name="RBACUserIdentity", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.identity.name}_{self.RBACUser.nickName}"

    class Meta:
        db_table = 'CSOOA_RBAC_RBACUser_Identity'
        verbose_name = "5.员工/岗位关系表"
        verbose_name_plural = verbose_name


class RBACUserPermissions(BaseModel):
    """
    员工/权限关系表
    """

    RBACUser = models.ForeignKey("RBAC.RBACUser", on_delete=models.CASCADE, verbose_name="员工",
                                 related_name="RBACUserPermissions", db_constraint=False)
    Permissions = models.ForeignKey("RBAC.Permissions", on_delete=models.CASCADE, verbose_name="权限",
                                    related_name="RBACUserPermissions", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.RBACUser.nickName}_{self.Permissions.name}"

    class Meta:
        db_table = 'CSOOA_RBAC_RBACUser_Permissions'
        verbose_name = "6.用户/权限关系表"
        verbose_name_plural = verbose_name


class IdentityPermissions(BaseModel):
    """
    岗位/权限关系表
    """

    identity = models.ForeignKey("RBAC.Identity", on_delete=models.CASCADE, verbose_name="部门",
                                 related_name="IdentityPermissions", db_constraint=False)
    Permissions = models.ForeignKey("RBAC.Permissions", on_delete=models.CASCADE, verbose_name="权限",
                                    related_name="IdentityPermissions", db_constraint=False)

    def __str__(self):
        return f"RBAC_{self.identity.name}_{self.Permissions.name}"

    class Meta:
        db_table = 'CSOOA_RBAC_identity_permissions'
        verbose_name = "7.岗位/权限关系表"
        verbose_name_plural = verbose_name
