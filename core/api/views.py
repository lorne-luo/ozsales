# coding=utf-8
import sys
from django.http import Http404
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ViewDoesNotExist, ObjectDoesNotExist
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from .filters import (AjaxDatatableOrderingFilter,
                                         AjaxDatatablePagination,
                                         AjaxDatatableSearchFilter,
                                         pk_in_filter_factory)


def get_app_model_name(kwargs):
    app_name = kwargs.get('app_name').lower()
    model_name = kwargs.get('model_name').lower()
    return app_name, model_name


def get_model_content_type(app_name, model_name):
    try:
        return ContentType.objects.get(app_label=app_name, model=model_name)
    except ObjectDoesNotExist:
        raise ViewDoesNotExist('No model found.')


class ContentTypeObjectView(GenericAPIView):
    model = None

    @property
    def app_name(self):
        if self.model:
            return self.model._meta.app_label
        else:
            raise ViewDoesNotExist

    @property
    def model_name(self):
        if self.model:
            return self.model._meta.model_name
        else:
            raise ViewDoesNotExist('No model found.')

    def get_model(self):
        if not self.model:
            app_name = self.kwargs.get('app_name').lower()
            model_name = self.kwargs.get('model_name').lower()
            try:
                model_content_type = ContentType.objects.get(app_label=app_name, model=model_name)
            except ObjectDoesNotExist:
                raise ViewDoesNotExist
            self.model = model_content_type.model_class()

    def get_serializer_class(self):
        if getattr(self, 'serializer_class', None):
            return self.serializer_class
        self.get_model()

        serialize_name = self.model.__name__ + 'Serializer'
        module_str = 'core.%s.serializers' % self.app_name
        if module_str not in sys.modules:
            module_str = 'apps.%s.serializers' % self.app_name
        serializer_module = sys.modules[module_str]

        self.serializer_class = getattr(serializer_module, serialize_name)
        return self.serializer_class

    def get_queryset(self):
        self.get_model()

        self.serializer_class = self.get_serializer_class()
        self.queryset = self.model.objects.all()
        self.filter_fields = getattr(self.model.Config, 'filter_fields', ())
        self.search_fields = getattr(self.model.Config, 'search_fields', ())

        q = super(ContentTypeObjectView, self).get_queryset()
        if hasattr(self.model.Config, 'filter_queryset'):
            q = self.model.Config.filter_queryset(self.request, q)
        return q


class CommonListCreateAPIView(ListCreateAPIView, ContentTypeObjectView):
    filter_backends = (filters.SearchFilter,
                       filters.DjangoFilterBackend,
                       filters.OrderingFilter)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommonRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView, ContentTypeObjectView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AjaxDatableView(object):
    """ status and page endpoint for ajax mode datatable """

    def get_model(self):
        if hasattr(self, 'queryset'):
            return getattr(self, 'queryset').model
        elif hasattr(self, 'model'):
            return getattr(self, 'model')
        else:
            raise ImproperlyConfigured('Can\'t get model for viewset')

    @list_route()
    def status(self, request, *args, **kwargs):
        self.filter_class = pk_in_filter_factory(self.get_model())
        return super(AjaxDatableView, self).list(self, request, *args, **kwargs)

    @list_route()
    def page(self, request, *args, **kwargs):
        """ pagination for ajax mode dataTable """
        self.pagination_class = AjaxDatatablePagination

        # get all events for channel
        self.filter_backends = getattr(self, 'filter_backends', []) + [AjaxDatatableOrderingFilter, AjaxDatatableSearchFilter]
        queryset = self.get_queryset()
        records_total = queryset.count()  # get total count
        queryset = self.filter_queryset(queryset)
        records_filtered_total = queryset.count()  # get filtered count

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        result = {
            "draw": request.query_params.get('draw', 0),
            "recordsTotal": records_total,
            "recordsFiltered": records_filtered_total,
            "data": [],
            "error": ""
        }
        result['data'] = serializer.data
        return Response(result)
