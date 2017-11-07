from django.shortcuts import render


# Create your views here.

class OwnerViewSetMixin(object):
    def get_queryset(self):
        qs = super(OwnerViewSetMixin, self).get_queryset()
        if self.request.user.is_seller:
            return qs.filter(seller=self.request.user.profile)
        elif self.request.user.is_customer:
            return qs.filter(customer=self.request.user.profile)
        else:
            return qs.none()
