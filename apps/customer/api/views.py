import logging
import json

import serializers
from ..models import Customer
from utils.api.views import PaginateMaxModelViewSet, PaginateMaxListAPIView
from utils.api.permission import ModelPermissions

log = logging.getLogger(__name__)


class CustomerViewSet(PaginateMaxModelViewSet):
    """
     A viewset for viewing and editing  instances.
    """
    serializer_class = serializers.CustomerSerializer
    queryset = Customer.objects.filter()


