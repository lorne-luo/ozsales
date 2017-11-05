from dal import autocomplete
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count, Case, IntegerField, When
from apps.express.models import ExpressCarrier, ExpressOrder


class ExpressCarrierAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            raise PermissionDenied

        seller_id = self.request.user.profile.id
        # order by carrier usage
        qs = ExpressCarrier.objects.all().annotate(use_counter=Count(Case(
            When(expressorder__order__seller=seller_id, then=1),
            default=0,
            output_field=IntegerField()
        ))).order_by('-use_counter')

        if self.q:
            qs = qs.filter(Q(name_cn__icontains=self.q))
        return qs
