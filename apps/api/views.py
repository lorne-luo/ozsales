# coding=utf-8

import sys
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from django.contrib.contenttypes.models import ContentType


def get_app_model_name(kwargs):
    app_name = kwargs.get('app_name').lower()
    model_name = kwargs.get('model_name').lower()
    return app_name, model_name

def get_model_content_type(app_name, model_name):
    return ContentType.objects.get(app_label=app_name, model=model_name)

class ContentTypeObjectView(GenericAPIView):

    def get_serializer_class(self):
        if getattr(self, 'serializer_class', None):
            return self.serializer_class
        self.app_name, self.model_name = get_app_model_name(self.kwargs)
        model_type = get_model_content_type(self.app_name, self.model_name)
        self.model = model_type.model_class()

        serialize_name = self.model.__name__ + 'Serializer'
        serializer_module = sys.modules['apps.%s.serializers' % self.app_name]
        self.serializer_class = getattr(serializer_module, serialize_name)
        return self.serializer_class

    def get_queryset(self):
        self.app_name, self.model_name = get_app_model_name(self.kwargs)
        model_type = get_model_content_type(self.app_name, self.model_name)
        self.model = model_type.model_class()

        serialize_name = self.model.__name__ + 'Serializer'
        serializer_module = sys.modules['apps.%s.serializers' % self.app_name]

        self.queryset = self.model.objects.all()
        self.filter_fields = getattr(self.model.Config, 'filter_fields', ())
        self.search_fields = getattr(self.model.Config, 'search_fields', ())
        self.serializer_class = getattr(serializer_module, serialize_name)

        q = super(ContentTypeObjectView, self).get_queryset()
        if hasattr(self.model.Config, 'filter_queryset'):
            q = self.model.Config.filter_queryset(self.request, q)
        return q


class CommonListCreateAPIView(ListCreateAPIView, ContentTypeObjectView):
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommonRetrieveUpdateAPIView(RetrieveUpdateAPIView, ContentTypeObjectView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)