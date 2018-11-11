# coding=utf-8
from braces.views import SuperuserRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

from core.django.views import CommonContextMixin
from .models import CarrierTracker
from . import forms


# views for CarrierTracker
class CarrierTrackerListView(SuperuserRequiredMixin, CommonContextMixin, ListView):
    model = CarrierTracker
    template_name = 'carrier_tracker/carriertracker_list.html'

    def get_context_data(self, **kwargs):
        return super(CarrierTrackerListView, self).get_context_data(**kwargs)


class CarrierTrackerAddView(SuperuserRequiredMixin, CommonContextMixin, CreateView):
    model = CarrierTracker
    form_class = forms.CarrierTrackerAdminForm
    template_name = 'carrier_tracker/carriertracker_add_edit.html'


class CarrierTrackerUpdateView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = CarrierTracker
    form_class = forms.CarrierTrackerAdminForm
    template_name = 'carrier_tracker/carriertracker_add_edit.html'


class CarrierTrackerDetailView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = CarrierTracker
    form_class = forms.CarrierTrackerDetailForm
    template_name = 'adminlte/common_detail_new.html'
