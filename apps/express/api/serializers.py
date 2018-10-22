# coding=utf-8
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import ExpressOrder, ExpressCarrier


class ExpressCarrierSerializer(BaseSerializer):
    id_upload_url = serializers.CharField()
    track_id_regex = serializers.CharField()

    class Meta:
        model = ExpressCarrier
        fields = ['pk', 'edit_url', 'detail_url', 'name_cn', 'name_en', 'website', 'id_upload_url',
                  'track_id_regex', 'is_default']
        read_only_fields = ['pk']


# Serializer for expressorder
class ExpressOrderSerializer(BaseSerializer):
    class Meta:
        model = ExpressOrder
        fields = ['pk', 'carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']
        read_only_fields = ['pk']

    def validate(self, attrs):
        carrier = attrs.get('carrier')
        track_id = attrs.get('track_id')
        if not carrier and not ExpressCarrier.identify_carrier(track_id):
            raise serializers.ValidationError('未能自动识别物流公司，请手动选择')
        return super(ExpressOrderSerializer, self).validate(attrs)
