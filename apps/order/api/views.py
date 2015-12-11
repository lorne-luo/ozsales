import logging
import json

from apps.order.api import serializers
from ..models import Order
from utils.api.views import PaginateMaxModelViewSet, PaginateMaxListAPIView
from utils.api.permission import ModelPermissions

log = logging.getLogger(__name__)


class OrderViewSet(PaginateMaxModelViewSet):
    """
     A viewset for viewing and editing  instances.
    """
    serializer_class = serializers.OrderSerializer
    queryset = Order.objects.filter()
    order_by = ['create_time']
