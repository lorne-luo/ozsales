# coding=utf-8
from rest_framework import serializers
from ...express_carrier.models import ExpressCarrier

from ..models import ExpressOrder


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
            raise serializers.ValidationError('未能自动识别物流公司，请手动选择')
        return super(ExpressOrderSerializer, self).validate(attrs)
