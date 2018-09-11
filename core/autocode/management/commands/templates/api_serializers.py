SERIALIZERS_HEADER = '''# coding=utf-8
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import <% ALL_MODELS %>

'''

SERIALIZERS_BODY = '''
class <% MODEL_NAME %>Serializer(BaseSerializer):
    """ Serializer for <% MODEL_NAME %> """

    class Meta:
        model = <% MODEL_NAME %>
        fields = ['pk', 'edit_url', 'detail_url'] + \\
                 <% fields %>
        read_only_fields = ['pk']

'''
