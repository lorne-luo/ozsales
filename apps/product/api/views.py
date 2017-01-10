import logging
from ..models import Product
from utils.api.views import PaginateMaxModelViewSet
import serializers

log = logging.getLogger(__name__)


class ProductViewSet(PaginateMaxModelViewSet):
    """
     A viewset for viewing and editing  instances.
    """
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
