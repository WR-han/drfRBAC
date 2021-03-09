from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.LimitOffsetPagination):
    """
    自定义分页返回结构
    """

    def get_paginated_response(self, serializer):
        try:
            field_header = serializer.field_header
        except Exception as e:
            field_header = [f"{e}"]
        return Response({
            "code": 200,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "count": self.count,
            "data": serializer.data,
            "field_header": field_header
        })
