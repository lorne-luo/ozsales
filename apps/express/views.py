# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.views.views import CommonContextMixin, CommonViewSet
from models import ExpressCarrier, ExpressOrder
from ..order.models import ORDER_STATUS
import forms


# views for ExpressCarrier

class ExpressCarrierListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = ExpressCarrier
    template_name_suffix = '_list'  # express/expresscarrier_list.html
    permissions = {
        "all": ("express.view_expresscarrier",)
    }


class ExpressCarrierAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("express.add_expresscarrier",)
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.seller = self.request.profile
        return super(ExpressCarrierAddView, self).form_valid(form)


class ExpressCarrierUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("express.change_expresscarrier",)
    }


class ExpressCarrierDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("express.view_expresscarrier",)
    }
