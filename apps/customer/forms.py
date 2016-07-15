# coding=utf-8
from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from models import Address, Customer, InterestTag


class CustomerAddForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomerAddForm, self).__init__(*args, **kwargs)
        # for add
        if 'initial' in kwargs and kwargs['initial']:
            pass
        # for change
        elif 'instance' in kwargs and kwargs['instance']:
            self.fields['primary_address'].queryset = Address.objects.filter(customer=kwargs['instance'].id)
            # self.fields['primary_address'].empty_label = None
            self.fields['primary_address'].empty_value = []


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


from django import forms


class CustomerAddForm2(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'groups', 'tags']

    def __init__(self, *args, **kwargs):
        super(CustomerAddForm2, self).__init__(*args, **kwargs)
        self.fields['groups'].help_text = ''
        self.fields['tags'].help_text = ''


class CustomerEditForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'primary_address', 'groups', 'tags', 'order_count']

    def __init__(self, *args, **kwargs):
        super(CustomerEditForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['primary_address'].queryset = Address.objects.filter(customer=instance)
            self.fields['order_count'].widget.attrs['readonly'] = True

        self.fields['groups'].help_text = ''
        self.fields['tags'].help_text = ''

    def remove_holddown(self):
        """This removes the unhelpful "Hold down the...." help texts for the specified fields for a form."""
        remove_message = unicode(_('Hold down "Control", or "Command" on a Mac, to select more than one.'))
        for field in self.fields:
            tx = self.fields[field].help_text
            if self.fields[field].help_text:
                self.fields[field].help_text = _(self.fields[field].help_text.replace(remove_message, '').strip())


class AddressAddForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'id_photo_back']


class AddressUpdateForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'id_photo_back']


class AddressDetailForm(ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'id_photo_back']


class CustomerAddForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'remarks', 'tags']


class CustomerDetailForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'order_count', 'primary_address', 'remarks', 'tags']


class CustomerUpdateForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'primary_address', 'order_count', 'remarks', 'tags']

    def __init__(self, *args, **kwargs):
        super(CustomerUpdateForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            instance = kwargs['instance']
            self.fields['primary_address'].queryset = Address.objects.filter(customer=instance)
            self.fields['order_count'].widget.attrs['readonly'] = True
