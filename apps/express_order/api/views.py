from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from core.api.filters import PinyinSearchFilter
from core.api.permission import SellerPermissions
from core.api.views import CommonViewSet
from ..models import ExpressOrder
from . import serializers


# api views for ExpressOrder
class ExpressOrderViewSet(CommonViewSet):
    """ api views for ExpressOrder """
    queryset = ExpressOrder.objects.all()
    model = ExpressOrder
    serializer_class = serializers.ExpressOrderSerializer
    # filter_class = OrderFilter
    filter_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']
    search_fields = ['carrier__name_cn', 'address__name', 'order__customer__name']
    permission_classes = (SellerPermissions,)
    # search only input are all ascii chars
    pinyin_search_fields = ['carrier__name_en', 'carrier__pinyin', 'track_id', 'order__customer__pinyin']
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)

    def get_queryset(self):
        queryset = super(ExpressOrderViewSet, self).get_queryset()
        if self.request.user.is_admin or self.request.user.is_superuser:
            return queryset
        return queryset.filter(order__seller=self.request.profile)

