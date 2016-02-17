from rest_framework import serializers
from ..models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    ''' Serializer for class '''
    primary_address_display = serializers.CharField(source='primary_address')

    class Meta:
        model = Customer
