import logging
from functools import reduce
from urllib.parse import unquote

from dal import autocomplete
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, filters

from core.api.filters import PinyinSearchFilter
from core.api.views import CommonViewSet
from core.django.autocomplete import HansSelect2ViewMixin
from core.django.permission import SellerRequiredMixin
from core.utils.string import include_non_asc
from . import serializers
from ..models import Product, Brand

log = logging.getLogger(__name__)


class ProductViewSet(CommonViewSet):
    """ API views for Product """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = ['name_en', 'name_cn', 'brand__id', 'brand__name_cn', 'brand__name_en']
    search_fields = ['name_cn', 'brand_cn']
    pinyin_search_fields = ['name_en', 'brand_en', 'pinyin', 'brand__name_en']  # search only input are all ascii chars
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)


class BrandViewSet(CommonViewSet):
    """ API views for Brand """
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    filter_fields = ['name_en', 'name_cn']
    search_fields = ['name_cn']
    pinyin_search_fields = ['name_en']  # search only input are all ascii chars
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)


class ProductAutocomplete(SellerRequiredMixin, HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = Product
    paginate_by = 20
    create_field = 'name_cn'

    def get_or_create_brand(self, brand_name):
        if include_non_asc(brand_name):
            brand, created = Brand.objects.get_or_create(name_cn=brand_name)
        else:
            brand, created = Brand.objects.get_or_create(name_en=brand_name)
        return brand

    def create_object(self, text):
        if '@' in text:
            brand_name = text.split('@')[0]
            product_name = text[text.index('@') + 1:]
            brand = self.get_or_create_brand(brand_name)
            if include_non_asc(product_name):
                product, created = Product.objects.get_or_create(brand=brand, name_cn=product_name,
                                                                 seller=self.request.profile)
            else:
                product, created = Product.objects.get_or_create(brand=brand, name_en=product_name,
                                                                 seller=self.request.profile)
            return product
        return self.get_queryset().create(**{self.create_field: text, 'seller': self.request.profile})

    def get_queryset(self):
        qs = Product.objects.all().order_by('brand__name_en', 'name_cn')
        keywords = unquote(self.q).split(' ')

        condition_list = [self.get_condition(keyword) for keyword in keywords]

        conditions = reduce(lambda a, b: a | b, condition_list)

        qs = qs.filter(*condition_list)
        return qs

    def get_condition(self, keyword):
        if include_non_asc(keyword):
            return Q(name_cn__icontains=keyword) | Q(brand__name_cn__icontains=keyword)
        else:
            # all ascii, number and letter
            keyword = keyword.lower()
            return Q(pinyin__contains=keyword) | Q(name_en__icontains=keyword) | Q(brand__name_en__icontains=keyword)
