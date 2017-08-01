# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Sum
from core.views.views import CommonContextMixin, CommonViewSet
from models import MonthlyReport
from apps.customer.models import Customer
from apps.order.models import Order, Address
from apps.express.models import ExpressOrder
import serializers
import forms


class MonthlyReportListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for MonthlyReport """
    model = MonthlyReport
    template_name_suffix = '_list'  # report/monthlyreport_list.html
    permissions = {
        "all": ("report.view_monthlyreport",)
    }


class MonthlyReportAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("monthlyreport.add_monthlyreport",)
    }


class MonthlyReportUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("monthlyreport.change_monthlyreport",)
    }


class MonthlyReportDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("monthlyreport.view_monthlyreport",)
    }


class MonthlyReportViewSet(CommonViewSet):
    """ API views for MonthlyReport """
    queryset = MonthlyReport.objects.all()
    serializer_class = serializers.MonthlyReportSerializer
    filter_fields = ['id']
    search_fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb',
                     'profit_rmb']


class TotalReport(TemplateView):
    template_name = 'report/total_report.html'

    def get_context_data(self, **kwargs):
        first_day = Order.objects.all().order_by('create_time').first().create_time
        distance = timezone.now() - first_day

        return {'total_year': distance.days / 365,
                'total_day': distance.days % 365,
                'total_customer': Customer.objects.count(),
                'total_order': Order.objects.count(),
                'total_address': Address.objects.count(),
                'total_expressorder': ExpressOrder.objects.count(),
                'total_amount': Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'],
                'total_sell_price': Order.objects.aggregate(Sum('sell_price_rmb'))['sell_price_rmb__sum'],
                'total_cost_aud': Order.objects.aggregate(Sum('product_cost_aud'))['product_cost_aud__sum'],
                'total_profit_rmb': Order.objects.aggregate(Sum('profit_rmb'))['profit_rmb__sum'],
                }
