# coding=utf-8
from django.http import Http404
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django.utils import timezone
from django.db.models import Sum

from core.auth_user.views import OwnerViewSetMixin
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


class TotalReport(TemplateView):
    template_name = 'report/total_report.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_seller:
            return Http404
        seller = self.request.user.profile
        first_day = Order.objects.filter(seller=seller).order_by('create_time').first().create_time
        distance = timezone.now() - first_day

        own_orders = Order.objects.filter(seller=seller)
        data = own_orders.aggregate(total_amount=Sum('total_amount'), total_sell_price=Sum('sell_price_rmb'),
                                    total_cost_aud=Sum('product_cost_aud'), total_profit_rmb=Sum('profit_rmb'),
                                    total_express_fee=Sum('shipping_fee'))

        context = super(TotalReport, self).get_context_data(**kwargs)
        context.update(data)
        context.update({'total_year': distance.days / 365,
                        'total_day': distance.days % 365,
                        'total_customer': Customer.objects.filter(seller=seller).count(),
                        'total_order': own_orders.count(),
                        'total_address': Address.objects.filter(customer__seller=seller).count(),
                        'total_expressorder': ExpressOrder.objects.filter(order__seller=seller).count(),
                        })
        return context
