# coding=utf-8
from braces.views import SuperuserRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

from core.django.views import CommonContextMixin
from .models import DefaultCarrier
from . import forms


# views for DefaultCarrier

class DefaultCarrierListView(SuperuserRequiredMixin, CommonContextMixin, ListView):
    model = DefaultCarrier
    template_name_suffix = '_list'  # default_carrier/defaultcarrier_list.html

    def get_context_data(self, **kwargs):
        return super(DefaultCarrier, self).get_context_data(**kwargs)


class DefaultCarrierAddView(SuperuserRequiredMixin, CommonContextMixin, CreateView):
    model = DefaultCarrier
    template_name = 'adminlte/common_form.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.DefaultCarrierAdminForm
        else:
            return forms.DefaultCarrierAddForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if not self.request.user.is_superuser:
            self.object.seller = self.request.profile
        return super(DefaultCarrierAddView, self).form_valid(form)


class DefaultCarrierUpdateView(SuperuserRequiredMixin, CommonContextMixin,
                               UpdateView):
    model = DefaultCarrier
    template_name = 'adminlte/common_form.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.DefaultCarrierAdminForm
        else:
            return forms.DefaultCarrierUpdateForm


class DefaultCarrierDetailView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = DefaultCarrier
    form_class = forms.DefaultCarrierDetailForm
    template_name = 'adminlte/common_detail_new.html'
