__author__ = 'Lorne'
from models import Address,Customer
from django import forms

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
            self.fields['primary_address'].empty_label = None
            self.fields['primary_address'].empty_value = []

