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


class DealTaskListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for DealTask """
    model = DealSubscribe
    template_name_suffix = '_list'  # schedule/dealtask_list.html
    permissions = {
        "all": ("schedule.view_dealtask",)
    }


class DealTaskAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for DealTask """
    model = DealSubscribe
    form_class = forms.DealTaskAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("dealtask.add_dealtask",)
    }


class DealTaskUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for DealTask """
    model = DealSubscribe
    form_class = forms.DealTaskUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("dealtask.change_dealtask",)
    }


class DealTaskDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for DealTask """
    model = DealSubscribe
    form_class = forms.DealTaskDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("dealtask.view_dealtask",)
    }


class DealTaskViewSet(CommonViewSet):
    """ API views for DealTask """
    queryset = DealSubscribe.objects.all()
    serializer_class = serializers.DealTaskSerializer
    filter_fields = ['id'] + ['includes', 'excludes', 'is_active']
    search_fields = ['includes', 'excludes', 'is_active']

