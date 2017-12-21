# coding=utf-8
import logging
from ..models import Order
from utils.api.views import PaginateMaxModelViewSet
import serializers

log = logging.getLogger(__name__)


class OrderViewSet(PaginateMaxModelViewSet):
    """
     A viewset for viewing and editing  instances.
    """
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.filter()
    order_by = ['create_time']
