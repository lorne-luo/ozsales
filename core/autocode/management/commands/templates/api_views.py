API_VIEWS_HEADER = '''# coding=utf-8
from rest_framework import permissions
from core.api.views import CommonViewSet
from ..models import <% MODEL_NAME %>
from . import serializers

'''

API_VIEWS_BODY = '''
class <% MODEL_NAME %>ViewSet(CommonViewSet):
    """ API views for <% MODEL_NAME %> """
    queryset = <% MODEL_NAME %>.objects.all()
    serializer_class = serializers.<% MODEL_NAME %>Serializer
    filter_fields = ['id'] + <% fields %>
    search_fields = <% fields %>

'''