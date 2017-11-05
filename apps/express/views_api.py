from dal import autocomplete
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count, Case, IntegerField, When
from apps.express.models import ExpressCarrier, ExpressOrder


class ExpressCarrierAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            raise PermissionDenied

        # order by carrier usage
        qs = ExpressCarrier.objects.order_by_usage(self.request.user)

        if self.q:
            qs = qs.filter(Q(name_cn__icontains=self.q))
        return qs
