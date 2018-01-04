# coding=utf-8
from django import forms
from django.contrib import admin
from django.forms.models import modelformset_factory, inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from core.django.forms import NoManytoManyHintModelForm
from models import Address, Customer, InterestTag


# class CustomerAddForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = ['name', 'email', 'mobile', 'primary_address', 'tags']
#
#     def __init__(self, *args, **kwargs):
#         super(CustomerAddForm, self).__init__(*args, **kwargs)
#         # for add
#         if 'initial' in kwargs and kwargs['initial']:
#             pass
#         # for change
#         elif 'instance' in kwargs and kwargs['instance']:
#             self.fields['primary_address'].queryset = Address.objects.filter(customer=kwargs['instance'].id)
#             # self.fields['primary_address'].empty_label = None
#             self.fields['primary_address'].empty_value = []


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


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'primary_address', 'tags', 'order_count']

    def __init__(self, *args, **kwargs):
        super(CustomerEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['primary_address'].queryset = Address.objects.filter(customer=instance)
            self.fields['order_count'].widget.attrs['readonly'] = True

        self.fields['tags'].help_text = ''

    def remove_holddown(self):
        """This removes the unhelpful "Hold down the...." help texts for the specified fields for a form."""
        remove_message = unicode(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))
        for field in self.fields:
            tx = self.fields[field].help_text
            if self.fields[field].help_text:
                self.fields[field].help_text = _(self.fields[field].help_text.replace(remove_message, '').strip())


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
        fields = ['name', 'email', 'mobile', 'remark', 'tags']


class CustomerDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'order_count', 'primary_address', 'remark', 'tags']


class CustomerUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'primary_address', 'order_count', 'remark', 'tags']

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['primary_address'].queryset = Address.objects.filter(customer=instance)
            self.fields['order_count'].widget.attrs['readonly'] = True


class AddressInlineForm(NoManytoManyHintModelForm):

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
