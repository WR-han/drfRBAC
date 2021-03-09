"""
自定义过滤器
"""

from rest_framework.filters import SearchFilter


class NickNameSearchFilter(SearchFilter):
    """
    用户名
    """
    search_param = "nickName"

    def get_search_fields(self, view, request):
        return ["nickName"]
