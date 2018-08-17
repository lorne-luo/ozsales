# coding=utf-8
from django import forms
from django.contrib import admin
from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from core.django.forms import NoManytoManyHintModelForm
from .models import Address, Customer, InterestTag
from core.django.widgets import IDThumbnailImageInput


class AddressAddInline(admin.TabularInline):
    model = Address
    extra = 1
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'Address'


class AddressChangeInline(admin.TabularInline):
    model = Address
    extra = 0
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'Address'


class InterestTagInline(admin.TabularInline):
    model = InterestTag
    extra = 1
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'Tag'


class AddressAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'id_photo_back']


class AddressUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'id_photo_back']


class AddressDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'id_photo_back']


class CustomerAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'remark', 'email', 'mobile']


class CustomerDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'remark', 'email', 'mobile', 'primary_address']


class CustomerUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'remark', 'email', 'mobile', 'primary_address']

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['primary_address'].queryset = Address.objects.filter(customer=instance)


class AddressInlineForm(NoManytoManyHintModelForm):
    id_photo_front = forms.ImageField(label=_("ID photo front"), required=False,
                                      widget=IDThumbnailImageInput({'width': '100%', 'size': 'thumbnail'}))
    id_photo_back = forms.ImageField(label=_("ID photo back"), required=False,
                                     widget=IDThumbnailImageInput({'width': '100%', 'size': 'thumbnail'}))

    class Meta:
        model = Address
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddressInlineForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.widget.attrs['class'] = 'form-control'

        self.fields['customer'].widget = forms.HiddenInput()


AddressFormSet = modelformset_factory(Address, form=AddressInlineForm, can_order=False, can_delete=False, extra=1)
AddressFormSet2 = inlineformset_factory(Customer, Address, form=AddressInlineForm, extra=1)
