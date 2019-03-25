from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import Store, Page


# Serializer for page
# class PageSerializer(BaseSerializer):
#     class Meta:
#         model = Page
#         fields = ['pk', 'edit_url', 'detail_url'] + \
#                  ['title', 'url', 'store', 'price', 'original_price']
#         read_only_fields = ['pk']
