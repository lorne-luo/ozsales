# coding=utf-8
from django import forms
from django.contrib import admin
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm

from ..customer.models import Customer, Address
from models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # for add
        if 'initial' in kwargs and kwargs['initial'] and 'customer_id' in kwargs['initial']:
            customer_id = kwargs['initial']['customer_id']
            self.fields['customer'].queryset = Customer.objects.filter(pk=customer_id)
            self.fields['customer'].empty_label = None
            self.fields['customer'].empty_value = []
            self.fields['address'].queryset = Address.objects.filter(customer_id=customer_id)
            self.fields['address'].empty_label = None
            self.fields['address'].empty_value = []
        elif 'instance' in kwargs and kwargs['instance']:
            customer_id = kwargs['instance'].customer.id
            self.fields['customer'].queryset = Customer.objects.filter(pk=customer_id)
            self.fields['customer'].empty_label = None
            self.fields['customer'].empty_value = []
            self.fields['address'].queryset = Address.objects.filter(customer_id=customer_id)
            self.fields['address'].empty_label = None
            self.fields['address'].empty_value = []


class OrderInline(admin.TabularInline):
    exclude = ['address', 'shipping_fee', 'product_cost_aud', 'product_cost_rmb', 'ship_time', 'origin_sell_rmb',
               'finish_time']
    model = Order
    extra = 0
    # max_num = 1
    can_delete = False
    verbose_name_plural = 'History Orders'

    def has_add_permission(self, request, obj=None):
        return False

class OrderForm2(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user')
        super(OrderForm2, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = '__all__'
        # exclude = ['epg_events_updated_at']


class OrderAddForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'address']


class OrderUpdateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'address', 'is_paid', 'status', 'total_amount', 'product_cost_aud', 'product_cost_rmb', 'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb', 'origin_sell_rmb', 'sell_price_rmb', 'profit_rmb', 'finish_time']

    def __init__(self, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['status'].widget.attrs['readonly'] = True
            self.fields['total_amount'].widget.attrs['readonly'] = True

class OrderDetailForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'address', 'is_paid', 'status', 'total_amount', 'product_cost_aud', 'product_cost_rmb', 'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb', 'origin_sell_rmb', 'sell_price_rmb', 'profit_rmb', 'finish_time']

