import logging
from django.db.models import Q
from dal import autocomplete
from rest_framework import permissions

from core.utils.string import include_non_asc
from core.django.autocomplete import HansSelect2ViewMixin
from core.django.permission import SellerRequiredMixin
from core.api.views import CommonViewSet
from ..models import Product, Brand
from . import serializers

log = logging.getLogger(__name__)


class ProductViewSet(CommonViewSet):
    """ API views for Product """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = ['name_en', 'name_cn', 'brand__id', 'brand__name_cn', 'brand__name_en']
    search_fields = ['name_en', 'name_cn', 'brand_en', 'brand_cn', 'pinyin']


class BrandViewSet(CommonViewSet):
    """ API views for Brand """
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    filter_fields = ['name_en', 'name_cn']
    search_fields = ['name_en', 'name_cn']


class ProductAutocomplete(SellerRequiredMixin, HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = Product
    paginate_by = 20
    create_field = 'name_cn'

    def create_object(self, text):
        return self.get_queryset().create(**{self.create_field: text, 'seller': self.request.profile})

    def get_queryset(self):
        qs = Product.objects.all_for_seller(self.request.user).order_by('brand__name_en', 'name_cn')

        if include_non_asc(self.q):
            qs = qs.filter(Q(name_cn__icontains=self.q) | Q(brand__name_cn__icontains=self.q))
        else:
            # all ascii, number and letter
            key = self.q.lower()
            qs = qs.filter(
                Q(pinyin__contains=key) | Q(name_en__icontains=key) | Q(brand__name_en__icontains=key))
        return qs
