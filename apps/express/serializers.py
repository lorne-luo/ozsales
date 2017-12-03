# coding=utf-8
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from models import ExpressCarrier, ExpressOrder


# Serializer for expresscarrier
class ExpressCarrierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpressCarrier
        fields = ['id', 'name_cn', 'name_en', 'website', 'search_url', 'id_upload_url', 'track_id_regex', 'is_default']
        read_only_fields = ['id']


# Serializer for expressorder
class ExpressOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpressOrder
        fields = ['id', 'carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']
        read_only_fields = ['id']
