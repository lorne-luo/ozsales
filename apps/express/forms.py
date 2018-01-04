# coding=utf-8
from django import forms
from django.contrib import admin
from django.forms.models import inlineformset_factory

from apps.order.models import Order
from core.django.forms import NoManytoManyHintModelForm
from core.django.autocomplete import FormsetModelSelect2
from models import ExpressCarrier, ExpressOrder


class ExpressCarrierAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'post_search_url', 'id_upload_url', 'track_id_regex',
                  'rate', 'is_default']


class ExpressCarrierDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'post_search_url', 'id_upload_url', 'track_id_regex',
                  'rate', 'is_default']


class ExpressCarrierUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = ExpressCarrier
        fields = ['name_cn', 'name_en', 'website', 'search_url', 'post_search_url', 'id_upload_url', 'track_id_regex',
                  'rate', 'is_default']


# class ExpressOrderAddForm(NoManytoManyHintModelForm):
#     class Meta:
#         model = ExpressOrder
#         fields = ['carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']
#
#
# class ExpressOrderDetailForm(NoManytoManyHintModelForm):
#     class Meta:
#         model = ExpressOrder
#         fields = ['carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload', 'remarks']
#
#
# class ExpressOrderUpdateForm(NoManytoManyHintModelForm):
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


class ExpressOrderInlineEditForm(NoManytoManyHintModelForm):
    carrier = forms.ModelChoiceField(label=u'物流', queryset=ExpressCarrier.objects.all(), required=False,
                                     widget=FormsetModelSelect2(url='express:expresscarrier-autocomplete',
                                                                attrs={'data-placeholder': u'物流中英文名称...',
                                                                       'class': 'form-control'})
                                     )
    track_id = forms.CharField(label=u'单号', max_length=30, required=False, help_text=u'单 号',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    fee = forms.DecimalField(label=u'运费', max_digits=8, decimal_places=2, required=False, help_text=u'运 费',
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    id_upload = forms.BooleanField(label=u'身份证', required=False)

    class Meta:
        model = ExpressOrder
        fields = ['carrier', 'track_id', 'order', 'fee', 'id_upload']

    def __init__(self, *args, **kwargs):
        super(ExpressOrderInlineEditForm, self).__init__(*args, **kwargs)
        self.fields['order'].widget = forms.HiddenInput()
        self.fields['carrier'].widget.attrs['autocomplete'] = 'off'

    def clean_fee(self):
        return self.cleaned_data.get('fee') or 0

    def clean(self):
        carrier = self.cleaned_data.get('carrier')
        track_id = self.cleaned_data.get('track_id')
        if not carrier and not ExpressCarrier.identify_carrier(track_id):
            self.add_error('carrier', u'未能自动识别物流公司，请手动选择')

        return self.cleaned_data


ExpressOrderFormSet = inlineformset_factory(Order, ExpressOrder, form=ExpressOrderInlineEditForm, extra=1)
