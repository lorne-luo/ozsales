from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import Customer, Address


# Serializer for address
class AddressSerializer(BaseSerializer):
    class Meta:
        model = Address
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'id_photo_back']
        read_only_fields = ['id']


# Serializer for customer
class CustomerSerializer(BaseSerializer):
    primary_address_display = serializers.CharField(source='primary_address')
    address_set = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name', 'email', 'mobile', 'order_count', 'primary_address', 'remark', 'tags',
                  'primary_address_display', 'address_set']
        read_only_fields = ['id']
