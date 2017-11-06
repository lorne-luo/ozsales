# coding=utf-8
from dal import autocomplete
from django.contrib import admin
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from django import forms
from django.forms.models import modelformset_factory
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


class ExpressOrderInlineAddForm(ModelForm):
    class Meta:
        model = ExpressOrder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExpressOrderInlineAddForm, self).__init__(*args, **kwargs)
        self.fields['order'].widget = forms.HiddenInput()
        self.fields['order'].widget.attrs['class'] = 'form-control'
        self.fields['carrier'].widget.attrs['class'] = 'form-control'
        self.fields['carrier'].widget.attrs['autocomplete'] = 'off'
        self.fields['track_id'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['fee'].widget.attrs['class'] = 'form-control'
        self.fields['weight'].widget.attrs['class'] = 'form-control'
        self.fields['remarks'].widget = forms.HiddenInput()
        self.fields['remarks'].widget.attrs['class'] = 'form-control'


class ExpressOrderInlineEditForm(ModelForm):
    carrier = forms.ModelChoiceField(
        queryset=ExpressCarrier.objects.all().order_by('-is_default'),
        widget=autocomplete.ModelSelect2(url='express:expresscarrier-autocomplete',
                                         attrs={'data-placeholder': u'选择快递', })
    )

    class Meta:
        model = ExpressOrder
        fields = ['carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload']

    def __init__(self, *args, **kwargs):
        super(ExpressOrderInlineEditForm, self).__init__(*args, **kwargs)
        self.fields['order'].widget = forms.HiddenInput()
        self.fields['carrier'].widget.attrs['autocomplete'] = 'off'
        self.fields['carrier'].queryset = ExpressCarrier.objects.all().order_by('-is_default')


ExpressOrderFormSet = modelformset_factory(ExpressOrder, form=ExpressOrderInlineEditForm,
                                           can_order=False, can_delete=False, extra=1)
