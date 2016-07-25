from django.shortcuts import render

from rest_framework import permissions
from core.adminlte.views import CommonContextMixin, CommonViewSet
from .models import ExpressOrder
import serializers
from django_filters import Filter, FilterSet

# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from core.adminlte.views import CommonContextMixin, CommonViewSet
from models import ExpressCarrier, ExpressOrder
import serializers
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
        "all": ("expresscarrier.add_expresscarrier",)
    }


class ExpressCarrierUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("expresscarrier.change_expresscarrier",)
    }


class ExpressCarrierDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("expresscarrier.view_expresscarrier",)
    }


class ExpressCarrierViewSet(CommonViewSet):
    """ api views for ExpressCarrier """
    queryset = ExpressCarrier.objects.all()
    serializer_class = serializers.ExpressCarrierSerializer
    filter_fields = ['name_cn', 'name_en', 'website', 'search_url', 'rate', 'is_default']
    search_fields = ['name_cn', 'name_en', 'website', 'search_url', 'rate', 'is_default']


# # views for ExpressOrder
#
# class ExpressOrderListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
#     model = ExpressOrder
#     template_name_suffix = '_list'  # express/expressorder_list.html
#     permissions = {
#         "all": ("express.view_expressorder",)
#     }
#
#
# class ExpressOrderAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
#     model = ExpressOrder
#     form_class = forms.ExpressOrderAddForm
#     template_name = 'adminlte/common_form.html'
#     permissions = {
#         "all": ("expressorder.add_expressorder",)
#     }
#
#
# class ExpressOrderUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
#     model = ExpressOrder
#     form_class = forms.ExpressOrderUpdateForm
#     template_name = 'adminlte/common_form.html'
#     permissions = {
#         "all": ("expressorder.change_expressorder",)
#     }
#
#
# class ExpressOrderDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
#     model = ExpressOrder
#     form_class = forms.ExpressOrderDetailForm
#     template_name = 'adminlte/common_detail_new.html'
#     permissions = {
#         "all": ("expressorder.view_expressorder",)
#     }


# api views for ExpressOrder
class ExpressOrderViewSet(CommonViewSet):
    """ api views for ExpressOrder """
    queryset = ExpressOrder.objects.all()
    serializer_class = serializers.ExpressOrderSerializer
    # filter_class = OrderFilter
    filter_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']
    search_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']
