# coding=utf-8
import json
import sys

import subprocess
from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ViewDoesNotExist, ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_extensions.mixins import PaginateByMaxMixin
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
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
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
        self.filter_backends = getattr(self, 'filter_backends', []) + [AjaxDatatableOrderingFilter,
                                                                       AjaxDatatableSearchFilter]
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


class CommonViewSet(PaginateByMaxMixin, ModelViewSet):
    """ provide list/retrive/patch/delete restful api for model """
    max_paginate_by = 200
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)

    # subclass implement below to specify permission for acitons
    # permissions_map = {
    #     'retrieve': [CommonAPIPermissions],
    #     'create': [CommonAPIPermissions],
    #     'list': [CommonAPIPermissions],
    #     'update': [CommonAPIPermissions],
    #     'delete': [CommonAPIPermissions],  # customized action below
    #     'destroy': [CommonAPIPermissions],
    # }

    def get_permissions(self):
        if hasattr(self, 'permissions_map'):
            if self.action.lower() in self.permissions_map:
                self.permission_classes = self.permissions_map[self.action]

        return super(CommonViewSet, self).get_permissions()

    @list_route(methods=['post', 'delete'])
    def delete(self, request, pk=None):
        """ for batch delete """
        pk = request.POST.get('pk')
        pk = pk.split(',')
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(pk__in=pk)
        if queryset.count():
            queryset.delete()
        else:
            data = {'detail': 'Object not found, or permission denied.'}
            return Response(data, status=404)
        return JsonResponse({'success': True}, status=200)

    @list_route(methods=['post', 'get'])
    def page(self, request):
        """ pagenation api for jquery.dataTable """
        draw = request.GET.get('draw', 0)
        length = int(request.GET.get('length', 5))
        start = int(request.GET.get('start', 0))
        order_column = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')
        search_keyword = request.GET.get('search[value]', '')
        raise NotImplementedError


class GitCommitInfoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        data = subprocess.check_output(
            ['git', 'show', '-s', '--date=iso8601', '--format=\'{"commit": "%h", "date": "%ad", "comment": "%s"}\''])
        commit = data.decode("utf-8").strip().strip('\'')

        return Response(json.loads(commit))
