from django.db import models


class BaseModel(models.Model):
    """
    基础model
    """

    isValidChoices = ((1, "有效"), (0, "已删除"))

    isValid = models.BooleanField("是否有效", choices=isValidChoices, default=1)
    createTime = models.DateTimeField("数据创建时间", auto_now_add=True)
    lastUpdateTime = models.DateTimeField("数据修改时间", auto_now=True)

    class Meta:
        abstract = True


class AccountModel(BaseModel):
    """
    账户基础model
    """

    # openid = models.CharField("openid", max_length=128, default="", blank=True, unique=True)
    # unionid = models.CharField("unionid", max_length=128, default="", blank=True, unique=True)
    nickName = models.CharField("名字", max_length=10)
    account = models.CharField("账号", max_length=20)
    password = models.CharField("密码", max_length=64)

    class Meta:
        abstract = True
