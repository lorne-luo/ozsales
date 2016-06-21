__author__ = 'Lorne'
from django.contrib import admin
from django.forms import ModelForm
from django import forms
from django.forms.models import modelformset_factory
from models import ExpressOrder


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
        self.fields['track_id'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['fee'].widget.attrs['class'] = 'form-control'
        self.fields['weight'].widget.attrs['class'] = 'form-control'
        self.fields['id_upload'].widget.attrs['class'] = 'form-control'
        self.fields['remarks'].widget = forms.HiddenInput()
        self.fields['remarks'].widget.attrs['class'] = 'form-control'


class ExpressOrderInlineEditForm(ModelForm):
    class Meta:
        model = ExpressOrder
        fields = ['carrier', 'track_id', 'order', 'address', 'fee', 'weight', 'id_upload']

    def __init__(self, *args, **kwargs):
        super(ExpressOrderInlineEditForm, self).__init__(*args, **kwargs)
        self.fields['order'].widget = forms.HiddenInput()


ExpressOrderFormSet = modelformset_factory(ExpressOrder, form=ExpressOrderInlineEditForm,
                                           can_order=False, can_delete=False, extra=1)
