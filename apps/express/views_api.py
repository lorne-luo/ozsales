from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count, Case, IntegerField, When

from apps.express.models import ExpressCarrier, ExpressOrder
from core.api.permission import SellerPermissions
from core.libs.string import include_non_asc
from core.views.views import CommonViewSet
import serializers


class ExpressCarrierViewSet(CommonViewSet):
    """ api views for ExpressCarrier """
    queryset = ExpressCarrier.objects.all()
    serializer_class = serializers.ExpressCarrierSerializer
    filter_fields = ['name_cn', 'name_en', 'website', 'search_url', 'rate', 'is_default']
    search_fields = ['name_cn', 'name_en', 'website', 'search_url', 'rate', 'is_default']
    permission_classes = (SellerPermissions,)

    def get_queryset(self):
        queryset = super(ExpressCarrierViewSet, self).get_queryset()
        if self.request.user.is_admin or self.request.user.is_superuser:
            return queryset
        if self.action.lower() in ['update', 'delete', 'destroy']:
            queryset = queryset.filter(seller=self.request.profile)
        return queryset


# api views for ExpressOrder
class ExpressOrderViewSet(CommonViewSet):
    """ api views for ExpressOrder """
    queryset = ExpressOrder.objects.all()
    model = ExpressOrder
    serializer_class = serializers.ExpressOrderSerializer
    # filter_class = OrderFilter
    filter_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']
    search_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']
    permission_classes = (SellerPermissions,)

    def get_queryset(self):
        queryset = super(ExpressOrderViewSet, self).get_queryset()
        if self.request.user.is_admin or self.request.user.is_superuser:
            return queryset
        return queryset.filter(order__seller=self.request.profile)


class ExpressCarrierAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    model = ExpressCarrier
    paginate_by = 50
    create_field = 'name_cn'


    def get_queryset(self):
        # order by carrier usage
        qs = ExpressCarrier.objects.order_by_usage(self.request.user)

        if include_non_asc(self.q):
            qs = qs.filter(Q(name_cn__icontains=self.q))
        else:
            # all ascii, number and letter
            qs = qs.filter(pinyin__contains=self.q.lower())
        return qs
