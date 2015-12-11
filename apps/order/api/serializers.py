from rest_framework import serializers
from ..models import Order
from utils.api.fields import (MediaUrlField, DisplayNestedFKField,
                                        VariationImageAPIField, VariationUrlField,
                                        FormDataPrimaryKeyRelatedField)

class OrderSerializer(serializers.ModelSerializer):
    ''' Serializer for class '''
    customer_display = serializers.CharField(source='customer')
    address_display = serializers.CharField(source='address')

    class Meta:
        model = Order
