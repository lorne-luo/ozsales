# coding=utf-8
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from models import Page, Store


# Serializer for page
class PageSerializer(BaseSerializer):
    class Meta:
        model = Page
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['title', 'url', 'store', 'price', 'original_price']
        read_only_fields = ['id']


# Serializer for store
class StoreSerializer(BaseSerializer):
    class Meta:
        model = Store
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']
        read_only_fields = ['id']
