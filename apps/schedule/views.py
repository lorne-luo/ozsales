# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from core.views.views import CommonContextMixin, CommonViewSet
from models import DealSubscribe
import serializers
import forms


class DealSubscribeListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for DealSubscribe """
    model = DealSubscribe
    template_name_suffix = '_list'  # schedule/dealsubscribe_list.html
    permissions = {
        "all": ("schedule.view_dealsubscribe",)
    }


class DealSubscribeAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for DealSubscribe """
    model = DealSubscribe
    form_class = forms.DealSubscribeAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("schedule.add_dealsubscribe",)
    }


class DealSubscribeUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for DealSubscribe """
    model = DealSubscribe
    form_class = forms.DealSubscribeUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("schedule.change_dealsubscribe",)
    }


class DealSubscribeDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for DealSubscribe """
    model = DealSubscribe
    form_class = forms.DealSubscribeDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("schedule.view_dealsubscribe",)
    }


class DealSubscribeViewSet(CommonViewSet):
    """ API views for DealSubscribe """
    queryset = DealSubscribe.objects.all()
    serializer_class = serializers.DealSubscribeSerializer
    filter_fields = ['id'] + ['includes', 'excludes', 'is_active']
    search_fields = ['includes', 'excludes', 'is_active']

