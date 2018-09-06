# coding=utf-8
from braces.views import SuperuserRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

from core.django.views import CommonContextMixin
from .models import CarrierTracker
from . import forms


# views for CarrierTracker

class CarrierTrackerListView(SuperuserRequiredMixin, CommonContextMixin, ListView):
    model = CarrierTracker
    template_name_suffix = '_list'  # carrier_tracker/CarrierTracker_list.html

    def get_context_data(self, **kwargs):
        return super(CarrierTracker, self).get_context_data(**kwargs)


class CarrierTrackerAddView(SuperuserRequiredMixin, CommonContextMixin, CreateView):
    model = CarrierTracker
    template_name = 'adminlte/common_form.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.CarrierTrackerAdminForm
        else:
            return forms.CarrierTrackerAddForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.request.user.is_superuser:
            self.object.seller = self.request.profile
        return super(CarrierTrackerAddView, self).form_valid(form)


class CarrierTrackerUpdateView(SuperuserRequiredMixin, CommonContextMixin,
                               UpdateView):
    model = CarrierTracker
    template_name = 'adminlte/common_form.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.CarrierTrackerAdminForm
        else:
            return forms.CarrierTrackerUpdateForm


class CarrierTrackerDetailView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = CarrierTracker
    form_class = forms.CarrierTrackerDetailForm
    template_name = 'adminlte/common_detail_new.html'
