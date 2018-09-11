# coding=utf-8
from rest_framework import serializers
from core.api.serializers import BaseSerializer, SellerOwnerSerializerMixin
from ..models import CarrierTracker


# Serializer for expresscarrier
class CarrierTrackerSerializer(BaseSerializer):
    class Meta:
        model = CarrierTracker
        fields = ['pk', 'edit_url', 'detail_url', 'name_cn', 'name_en', 'website', 'search_url',
                  'id_upload_url', 'track_id_regex', 'need_id']
        read_only_fields = ['pk']
