import operator
from django_filters.filters import BaseInFilter
from django_filters import FilterSet
from django.db import models
from django.utils import six
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import filters, pagination
from rest_framework.compat import distinct

from core.django.helpers import include_non_asc
from functools import reduce


class AjaxDatatableOrderingFilter(OrderingFilter):
    """ for ajax datatable """
    ordering_param = 'order[0][column]'
    ordering_direction_param = 'order[0][dir]'

    def get_ordering(self, request, queryset, view):
        ordering_fields = getattr(view, 'ordering_fields', None)
        ordering_column = request.query_params.get(self.ordering_param, None)
        ordering_direction = request.query_params.get(self.ordering_direction_param, None)

        if not ordering_column or not ordering_fields:
            return None

        ordering_index = int(ordering_column)
        if ordering_index > len(ordering_fields):
            return None

        ordering_field = ordering_fields[ordering_index - 1]
        if ordering_direction.lower() == 'desc':
            ordering_field = '-' + ordering_field

        return [ordering_field]


class AjaxDatatablePagination(pagination.LimitOffsetPagination):
    """ for ajax datatable """
    limit_query_param = 'length'
    offset_query_param = 'start'


class AjaxDatatableSearchFilter(SearchFilter):
    search_param = 'search[value]'


class AbstractPKInFilter(FilterSet):
    """ for ajax datatable """
    id = BaseInFilter()

    class Meta:
        model = None

class PinyinSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        if any([include_non_asc(x) for x in search_terms]):
            search_fields = getattr(view, 'search_fields', None)
        else:
            search_fields = getattr(view, 'pinyin_search_fields', None)

        if getattr(view, 'search_id_for_number', False):
            if len(search_terms) == 1 and search_terms[0].isdigit() and not search_terms[0].startswith('0'):
                return queryset.filter(pk=search_terms[0])

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(six.text_type(search_field))
            for search_field in search_fields
        ]

        base = queryset
        conditions = []
        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            queryset = distinct(queryset, base)
        return queryset

def pk_in_filter_factory(model):
    super_class = AbstractPKInFilter
    name = '%sPKInFilter' % model.__name__
    Meta = type('Meta', (object,), {'model': model})
    return type(name, (super_class,), {'Meta': Meta,})
