# coding=utf-8
from braces.views import MultiplePermissionsRequiredMixin, SuperuserRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

from core.django.views import CommonContextMixin
from .models import DealSubscribe
from . import forms


class DealSubscribeListView(SuperuserRequiredMixin, CommonContextMixin, ListView):
    """ List views for DealSubscribe """
    model = DealSubscribe
    template_name_suffix = '_list'  # schedule/dealsubscribe_list.html


class DealSubscribeAddView(SuperuserRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for DealSubscribe """
    model = DealSubscribe
    form_class = forms.DealSubscribeAddForm
    template_name = 'adminlte/common_form.html'


class DealSubscribeUpdateView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for DealSubscribe """
    model = DealSubscribe
    form_class = forms.DealSubscribeUpdateForm
    template_name = 'adminlte/common_form.html'


class DealSubscribeDetailView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for DealSubscribe """
    model = DealSubscribe
    form_class = forms.DealSubscribeDetailForm
    template_name = 'adminlte/common_detail_new.html'
