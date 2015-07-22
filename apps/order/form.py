__author__ = 'Lorne'

from django import forms

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
