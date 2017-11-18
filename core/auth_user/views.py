from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseForbidden


# Create your views here.
from django.urls import reverse_lazy


class OwnerViewSetMixin(object):
    def get_queryset(self):
        qs = super(OwnerViewSetMixin, self).get_queryset()
        if self.request.user.is_seller:
            return qs.filter(seller=self.request.user.profile)
        elif self.request.user.is_customer:
            return qs.filter(customer=self.request.user.profile)
        else:
            return qs.none()


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('order:order-list-short'))
    else:
        return HttpResponseRedirect(reverse_lazy('member-login'))