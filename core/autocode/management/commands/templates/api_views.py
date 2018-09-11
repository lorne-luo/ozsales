API_VIEWS_HEADER = '''# coding=utf-8
from rest_framework import permissions
from core.api.views import CommonViewSet
from ..models import <% ALL_MODELS %>
from . import serializers

'''

API_VIEWS_BODY = '''
class <% MODEL_NAME %>ViewSet(CommonViewSet):
    """ API views for <% MODEL_NAME %> """
    queryset = <% MODEL_NAME %>.objects.all()
    serializer_class = serializers.<% MODEL_NAME %>Serializer
    filter_fields = ['pk'] + <% fields %>
    search_fields = <% fields %>
    ordering_fields = <% fields %>

'''
