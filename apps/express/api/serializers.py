# coding=utf-8
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import ExpressCarrier, ExpressOrder


# Serializer for expresscarrier
class ExpressCarrierSerializer(BaseSerializer):
    class Meta:
        model = ExpressCarrier
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name_cn', 'name_en', 'website', 'search_url', 'id_upload_url', 'track_id_regex', 'is_default']
        read_only_fields = ['id']


# Serializer for expressorder
class ExpressOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpressOrder
        fields = ['id', 'carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']
        read_only_fields = ['id']

    def validate(self, attrs):
        carrier = attrs.get('carrier')
        track_id = attrs.get('track_id')
        if not carrier and not ExpressCarrier.identify_carrier(track_id):
            raise serializers.ValidationError(u'未能自动识别物流公司，请手动选择')
        return super(ExpressOrderSerializer, self).validate(attrs)