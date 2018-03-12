# coding=utf-8
from core.api.views import CommonViewSet
from ..models import DealSubscribe
from . import serializers


class DealSubscribeViewSet(CommonViewSet):
    """ API views for DealSubscribe """
    queryset = DealSubscribe.objects.all()
    serializer_class = serializers.DealSubscribeSerializer
    filter_fields = ['id'] + ['includes', 'excludes', 'is_active']
    search_fields = ['includes', 'excludes', 'is_active']

