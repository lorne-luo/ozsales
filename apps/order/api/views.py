# coding=utf-8
import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import list_route, detail_route
from rest_framework import filters
from rest_framework.response import Response
from django_filters import FilterSet
from django.db.models import Q

from core.api.filters import PinyinSearchFilter
from core.api.permission import SellerPermissions
from core.api.views import CommonViewSet
from ..models import Order, ORDER_STATUS, OrderProduct
from . import serializers

log = logging.getLogger(__name__)


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['in', 'exact'],
            'customer__name': ['exact', 'contains']
        }


class NewOrderFilter(FilterSet):
    class Meta:
        model = Order
        exclude = []

    @property
    def qs(self):
        qs = super(NewOrderFilter, self).qs.filter(Q(status=ORDER_STATUS.CREATED) | Q(is_paid=False))
        return qs


class ShippingOrderFilter(FilterSet):
    class Meta:
        model = Order
        exclude = []

    @property
    def qs(self):
        qs = super(ShippingOrderFilter, self).qs.filter(
            Q(status=ORDER_STATUS.SHIPPING) | Q(status=ORDER_STATUS.DELIVERED), is_paid=True)
        return qs


class OrderViewSet(CommonViewSet):
    """ api views for Order """
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_class = OrderFilter
    filter_fields = ['uuid']
    search_fields = ['customer__name', 'address__name', 'address__address']
    permission_classes = (SellerPermissions,)
    pinyin_search_fields = ['customer__pinyin', 'address__pinyin']  # search only input are all ascii chars
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)

    def get_queryset(self):
        queryset = super(OrderViewSet, self).get_queryset()
        if self.request.user.is_admin or self.request.user.is_superuser:
            return queryset
        return queryset.filter(seller=self.request.profile).select_related('address', 'customer')

    @list_route(methods=['get'])
    def new(self, request, *args, **kwargs):
        # status==CREATED or is_paid=False
        self.filter_class = NewOrderFilter
        return super(OrderViewSet, self).list(self, request, *args, **kwargs)

    @list_route(methods=['get'])
    def shipping(self, request, *args, **kwargs):
        # status==SHIPPING or DELIVERD and is_paid=True
        self.filter_class = ShippingOrderFilter
        return super(OrderViewSet, self).list(self, request, *args, **kwargs)

    @detail_route(methods=['post'])
    def set_status(self, request, *args, **kwargs):
        order = self.get_object()
        status = request.POST.get('status', None)
        if status:
            order.set_status(status)

        data = self.serializer_class(order, context={'request': request}).data
        return Response(data)


class OrderProductViewSet(CommonViewSet):
    """ api views for OrderProduct """
    queryset = OrderProduct.objects.all()
    serializer_class = serializers.OrderProductSerializer
    filter_fields = ['uuid']
    search_fields = ['order__customer__name', 'order__address__name', 'name', 'product__name_cn',
                     'product__brand__name_cn']
    permission_classes = [SellerPermissions]
    pinyin_search_fields = ['product__name_en', 'product__brand__name_en']  # search only input are all ascii chars
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)
