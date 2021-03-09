import datetime
import jwt

from Module_Public.key import RBAC_token_salt


def make_rbac_token(user_id, expire_hour=24):
    """
    RBACToken生成器
    :param user_id: 用户id
    :param expire_hour: 过期时间(小时)
    :return: token
    """

    playload = {
        "id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=expire_hour),
        'iat': datetime.datetime.utcnow(),
    }

    token = jwt.encode(playload, RBAC_token_salt, algorithm='HS256')

    return token

