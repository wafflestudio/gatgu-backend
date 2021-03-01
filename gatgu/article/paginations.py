from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ArticlePagination(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return Response(self.get_paginated_data(data))

    def get_paginated_data(self, data):
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'articles': data
        }