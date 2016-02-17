from rest_framework import serializers
from ..models import Product

class ProductSerializer(serializers.ModelSerializer):
    ''' Serializer for class '''
    brand_display = serializers.CharField(source='brand')

    class Meta:
        model = Product
