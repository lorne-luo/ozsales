from rest_framework import filters, pagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.filters import BaseInFilter
from django_filters import FilterSet

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


def pk_in_filter_factory(model):
    super_class = AbstractPKInFilter
    name = '%sPKInFilter' % model.__name__
    Meta = type('Meta', (object,), {'model': model})
    return type(name, (super_class,), {'Meta': Meta,})
