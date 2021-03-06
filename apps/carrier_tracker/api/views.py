from dal import autocomplete
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from core.api.filters import PinyinSearchFilter
from core.api.permission import SellerPermissions
from core.api.views import CommonViewSet
from core.django.autocomplete import HansSelect2ViewMixin
from core.django.permission import SellerRequiredMixin
from core.utils.string import include_non_asc
from ..models import CarrierTracker
from . import serializers


class CarrierTrackerViewSet(CommonViewSet):
    """ api views for CarrierTracker """
    queryset = CarrierTracker.objects.all()
    serializer_class = serializers.CarrierTrackerSerializer
    filter_fields = ['name_cn', 'name_en', 'website', 'search_url', 'need_id']
    search_fields = ['name_cn']
    permission_classes = (SellerPermissions,)
    pinyin_search_fields = ['pinyin', 'name_en', 'website']  # search only input are all ascii chars
    filter_backends = (DjangoFilterBackend,
                       PinyinSearchFilter,
                       filters.OrderingFilter)

    def get_queryset(self):
        queryset = super(CarrierTrackerViewSet, self).get_queryset()
        if self.request.user.is_admin or self.request.user.is_superuser:
            return queryset
        if self.action.lower() in ['update', 'delete', 'destroy']:
            queryset = queryset.filter(seller=self.request.profile)
        return queryset


class CarrierTrackerAutocomplete(SellerRequiredMixin, HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = CarrierTracker
    paginate_by = 50
    create_field = 'name_cn'

    def create_object(self, text):
        return self.get_queryset().create(**{self.create_field: text, 'seller': self.request.profile})

    def get_queryset(self):
        # order by carrier usage
        qs = CarrierTracker.objects.all()

        if include_non_asc(self.q):
            qs = qs.filter(Q(name_cn__icontains=self.q))
        else:
            # all ascii, number and letter
            qs = qs.filter(pinyin__contains=self.q.lower())
        return qs
