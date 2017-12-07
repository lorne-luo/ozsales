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


class HansSelect2ViewMixin(object):
    def get_create_option(self, context, q):
        create_option = super(HansSelect2ViewMixin, self).get_create_option(context, q)
        if create_option:
            create_option[0]['text'] = u'新建 "%s"' % q
        return create_option
