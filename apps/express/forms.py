# coding=utf-8
from dal import autocomplete
from django.contrib import admin

from apps.order.models import Order
from core.forms.widgets import FormsetModelSelect2
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory
from models import ExpressCarrier, ExpressOrder


class ExpressCarrierAddForm(ModelForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'id_upload_url', 'track_id_regex', 'rate',
                  'is_default']


class ExpressCarrierDetailForm(ModelForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'id_upload_url', 'track_id_regex', 'rate',
                  'is_default']


class ExpressCarrierUpdateForm(ModelForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'id_upload_url', 'track_id_regex', 'rate',
                  'is_default']


# class ExpressOrderAddForm(ModelForm):
#     class Meta:
#         model = ExpressOrder
#         fields = ['carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']
#
#
# class ExpressOrderDetailForm(ModelForm):
#     class Meta:
#         model = ExpressOrder
#         fields = ['carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']
#
#
# class ExpressOrderUpdateForm(ModelForm):
#     class Meta:
#         model = ExpressOrder
#         fields = ['carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']


class ExpressOrderAddInline(admin.TabularInline):
    exclude = ['id_upload', 'create_time']
    model = ExpressOrder
    can_delete = True
    extra = 1
    # max_num = 1
    verbose_name_plural = 'ExpressOrder'


class ExpressOrderChangeInline(admin.TabularInline):
    model = ExpressOrder
    can_delete = True
    extra = 1
    # max_num = 1
    verbose_name_plural = 'ExpressOrder'


class ExpressOrderInlineEditForm(ModelForm):
    carrier = forms.ModelChoiceField(
        queryset=ExpressCarrier.objects.all(), required=False,
        widget=FormsetModelSelect2(url='express:expresscarrier-autocomplete',
                                         attrs={'data-placeholder': u'快递中英文名称...', 'class': 'form-control'})
    )
    track_id = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    fee = forms.DecimalField(max_digits=8, decimal_places=2, required=False,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    id_upload = forms.BooleanField(required=False)

    class Meta:
        model = ExpressOrder
        fields = ['carrier', 'track_id', 'order', 'fee', 'weight', 'id_upload']

    def __init__(self, *args, **kwargs):
        super(ExpressOrderInlineEditForm, self).__init__(*args, **kwargs)
        self.fields['order'].widget = forms.HiddenInput()
        self.fields['carrier'].widget.attrs['autocomplete'] = 'off'

    def clean_fee(self):
        return self.cleaned_data.get('fee') or 0


# ExpressOrderFormSet = modelformset_factory(ExpressOrder, form=ExpressOrderInlineEditForm, extra=1)
ExpressOrderFormSet = inlineformset_factory(Order, ExpressOrder, form=ExpressOrderInlineEditForm, extra=1)
