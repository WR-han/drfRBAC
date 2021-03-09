"""
自定义过滤器
"""

from rest_framework.filters import SearchFilter


class NickNameSearchFilter(SearchFilter):
    """
    DEMO 用户名过滤器
    """
    search_param = "nickName"  # url查询参数

    def get_search_fields(self, view, request):
        return ["nickName"]  # 可接受查询的字段范围
