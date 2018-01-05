# coding=utf-8
from core.django.forms import NoManytoManyHintModelForm
from models import MonthlyReport


class MonthlyReportAddForm(NoManytoManyHintModelForm):
    """ Add form for MonthlyReport """
    class Meta:
        model = MonthlyReport
        fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb', 'profit_rmb']


class MonthlyReportDetailForm(NoManytoManyHintModelForm):
    """ Detail form for MonthlyReport """
    class Meta:
        model = MonthlyReport
        fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb', 'profit_rmb']


class MonthlyReportUpdateForm(NoManytoManyHintModelForm):
    """ Update form for MonthlyReport """
    class Meta:
        model = MonthlyReport
        fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb', 'profit_rmb']

