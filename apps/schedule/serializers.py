# coding=utf-8
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from models import DealSubscribe


class DealTaskSerializer(BaseSerializer):
    """ Serializer for DealTask """

    class Meta:
        model = DealSubscribe
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['includes', 'excludes', 'is_active']
        read_only_fields = ['id']

