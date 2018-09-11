from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import Page, Store


# Serializer for page
class PageSerializer(BaseSerializer):
    class Meta:
        model = Page
        fields = ['pk', 'edit_url', 'detail_url'] + \
                 ['title', 'url', 'store', 'price', 'original_price']
        read_only_fields = ['pk']


# Serializer for store
class StoreSerializer(BaseSerializer):
    class Meta:
        model = Store
        fields = ['pk', 'edit_url', 'detail_url'] + \
                 ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']
        read_only_fields = ['pk']
