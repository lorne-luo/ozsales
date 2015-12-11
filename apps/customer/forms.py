from django import forms
from django.contrib import admin

from models import Address,Customer,InterestTag

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


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

