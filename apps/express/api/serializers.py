# coding=utf-8
from django.utils import timezone
from rest_framework import serializers

from apps.carrier_tracker.models import CarrierTracker
from core.api.serializers import BaseSerializer
from ..models import ExpressOrder, ExpressCarrier


class ExpressCarrierSerializer(BaseSerializer):
    id_upload_url = serializers.CharField()
    track_id_regex = serializers.CharField()

    class Meta:
        model = ExpressCarrier
        fields = ['pk', 'edit_url', 'detail_url', 'name_cn', 'name_en', 'website', 'id_upload_url',
                  'track_id_regex', 'parcel_count']
        read_only_fields = ['pk']


# Serializer for expressorder
class ExpressOrderSerializer(BaseSerializer):
    class Meta:
        model = ExpressOrder
        fields = ['pk', 'carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks',
                  'is_delivered']
        read_only_fields = ['pk']

    def validate(self, attrs):
        if not self.instance or not self.instance.pk:
            carrier = attrs.get('carrier')
            track_id = attrs.get('track_id')
            if not carrier and not CarrierTracker.identify_carrier(track_id):
                raise serializers.ValidationError('未能自动识别物流公司，请手动选择')

        return super(ExpressOrderSerializer, self).validate(attrs)
