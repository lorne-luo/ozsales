# coding=utf-8
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import MonthlyReport


class MonthlyReportAddForm(ModelForm):
    """ Add form for MonthlyReport """
    class Meta:
        model = MonthlyReport
        fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb', 'profit_rmb']


class MonthlyReportDetailForm(ModelForm):
    """ Detail form for MonthlyReport """
    class Meta:
        model = MonthlyReport
        fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb', 'profit_rmb']


class MonthlyReportUpdateForm(ModelForm):
    """ Update form for MonthlyReport """
    class Meta:
        model = MonthlyReport
        fields = ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb', 'profit_rmb']

