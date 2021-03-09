from rest_framework.permissions import BasePermission


class SecondaryPermission(BasePermission):

    def has_permission(self, request, view):

        user_permissions = request.user.get_permissions

        if "AdminPermission" in user_permissions:
            return True

        method = request.method
        if request.method == "PATCH":
            method = "PUT"
        need_permission = f"{method}_{type(self).__name__}"

        if need_permission in user_permissions:
            return True
        else:
            return False


class MainPermission(SecondaryPermission):

    def has_permission(self, request, view):
        base_action = ["list", "retrieve", "create", "update", "partial_update", "destroy"]
        is_check = super(MainPermission, self).has_permission(request, view)
        action = view.action

        if action not in base_action:
            # 动作类型不是基础action / 子路由
            if is_check:
                # 拥有主路由权限
                request.main_permission = True

            return True
        else:
            return is_check
