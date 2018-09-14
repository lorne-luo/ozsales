import logging
from dal import autocomplete
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from core.api.filters import PinyinSearchFilter
from core.django.autocomplete import HansSelect2ViewMixin
from core.django.permission import SellerRequiredMixin
from core.utils.string import include_non_asc
from core.api.permission import SellerPermissions
from core.api.views import CommonViewSet
from ..models import Customer, Address
from . import serializers

log = logging.getLogger(__name__)


class AddressViewSet(CommonViewSet):
    """api views for Address"""
    queryset = Address.objects.all()
    serializer_class = serializers.AddressSerializer
    filter_fields = ['name', 'mobile', 'address', 'customer', 'id_number']
    search_fields = ['name', 'address', 'customer__name']
    pinyin_search_fields = ['customer__pinyin', 'pinyin', 'mobile']  # search only input are all ascii chars
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)


class CustomerViewSet(CommonViewSet):
    """api views for Customer"""
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    filter_fields = ['name', 'email', 'mobile', 'order_count', 'primary_address',
                     'remark', 'tags']
    search_fields = ['name', 'primary_address__name', 'remark']
    permission_classes = (SellerPermissions,)
    pinyin_search_fields = ['pinyin', 'mobile']  # search only input are all ascii chars
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)


class CustomerAutocomplete(SellerRequiredMixin, HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = Customer
    paginate_by = 20

    def create_object(self, text):
        return self.get_queryset().create(**{self.create_field: text})

    def get_queryset(self):
        qs = Customer.objects.order_by('-order_count')

        if include_non_asc(self.q):
            qs = qs.filter(name__icontains=self.q)
        else:
            # all ascii, number and letter
            if self.q.isdigit():
                qs = qs.filter(mobile__icontains=self.q)
            else:
                qs = qs.filter(pinyin__contains=self.q.lower())
        return qs


class AddressAutocomplete(HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = Address
    paginate_by = 20
    create_field = 'address'

    def create_object(self, text):
        # todo extract name, phone number
        return self.get_queryset().create(**{self.create_field: text, 'customer_id': self.forwarded.get('customer')})

    def get_queryset(self):
        qs = Address.objects.all()
        cid = self.forwarded.get('customer')

        if cid:
            qs = qs.filter(customer_id=cid)

        if include_non_asc(self.q):
            qs = qs.filter(Q(name__icontains=self.q) | Q(address__icontains=self.q))
        else:
            # all ascii, number and letter
            if self.q.isdigit():
                qs = qs.filter(mobile__icontains=self.q)
            else:
                qs = qs.filter(pinyin__contains=self.q.lower())
        return qs
