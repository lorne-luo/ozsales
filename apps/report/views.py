# coding=utf-8
from braces.views import MultiplePermissionsRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

import forms
import serializers
from core.auth_user.views import OwnerViewSetMixin
from core.django.views import CommonContextMixin
from core.api.views import CommonViewSet
from models import MonthlyReport


class MonthlyReportListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for MonthlyReport """
    model = MonthlyReport
    template_name_suffix = '_list'  # report/monthlyreport_list.html
    permissions = {
        "all": ("report.view_monthlyreport",)
    }

    def get_context_data(self, **kwargs):
        context = super(MonthlyReportListView, self).get_context_data(**kwargs)
        data = MonthlyReport.stat_user_total(self.request.user)
        context.update(data)
        return context


class MonthlyReportAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("report.add_monthlyreport",)
    }


class MonthlyReportUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("report.change_monthlyreport",)
    }


class MonthlyReportDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for MonthlyReport """
    model = MonthlyReport
    form_class = forms.MonthlyReportDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("report.view_monthlyreport",)
    }


class MonthlyReportViewSet(OwnerViewSetMixin, CommonViewSet):
    """ API views for MonthlyReport """
    queryset = MonthlyReport.objects.all()
    serializer_class = serializers.MonthlyReportSerializer
    filter_fields = ['id']
    search_fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb',
                     'profit_rmb']
