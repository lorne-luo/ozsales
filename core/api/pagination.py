# coding=utf-8
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CommonPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        count = self.page.paginator.count
        total_page = self.page.paginator.num_pages
        return Response(OrderedDict([
            ('per_page', self.page_size),
            ('current_page', self.page.number),
            ('total_page', total_page),
            ('count', count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
