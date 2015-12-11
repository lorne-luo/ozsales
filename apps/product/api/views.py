import logging
import json

from apps.product.api import serializers
from ..models import Product
from utils.api.views import PaginateMaxModelViewSet, PaginateMaxListAPIView
from utils.api.permission import ModelPermissions

log = logging.getLogger(__name__)


class ProductViewSet(PaginateMaxModelViewSet):
    """
     A viewset for viewing and editing  instances.
    """
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.filter()
    order_by = ['create_time']


