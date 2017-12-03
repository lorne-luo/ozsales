# coding=utf-8
from django import forms
from django.contrib import admin
from django.forms.models import inlineformset_factory, modelformset_factory
from dal import autocomplete

from core.forms.widgets import FormsetModelSelect2
from core.forms.forms import NoManytoManyHintModelForm
from ..customer.models import Customer, Address
from ..product.models import Product
from models import Order, OrderProduct, ORDER_STATUS, ORDER_STATUS_CHOICES


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


class OrderInline(admin.TabularInline):
    exclude = ['address', 'shipping_fee', 'product_cost_aud', 'product_cost_rmb', 'ship_time', 'origin_sell_rmb',
               'finish_time']
    model = Order
    extra = 0
    # max_num = 1
    can_delete = False
    verbose_name_plural = 'History Orders'

    def has_add_permission(self, request, obj=None):
        return False


class OrderForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop('user')
        super(OrderForm2, self).__init__(*args, **kwargs)

    class Meta:
        model = Order
        fields = '__all__'
        # exclude = ['epg_events_updated_at']


class OrderAddForm(NoManytoManyHintModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=autocomplete.ModelSelect2(url='customer:customer-autocomplete',
                                         attrs={'data-placeholder': u'任意姓名、手机号...'})
    )

    class Meta:
        model = Order
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super(OrderAddForm, self).__init__(*args, **kwargs)


class OrderUpdateForm(NoManytoManyHintModelForm):
    address = forms.ModelChoiceField(
        queryset=Address.objects.all(),
        widget=FormsetModelSelect2(url='customer:address-autocomplete',
                                   forward=['customer'],
                                   attrs={'data-placeholder': u'任意姓名、地址、手机号...'})
    )
    status = forms.ChoiceField(label='Status', choices=ORDER_STATUS_CHOICES, required=False)
    cost_aud = forms.CharField(label='Cost AUD', required=False)
    sell_rmb = forms.CharField(label='Sell RMB', required=False)

    class Meta:
        model = Order
        fields = ['customer', 'address', 'total_amount', 'status', 'is_paid', 'paid_time', 'ship_time',
                  'cost_aud', 'sell_rmb', 'sell_price_rmb', 'finish_time']

    def __init__(self, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.customer:
            self.fields['total_amount'].widget.attrs['readonly'] = True
            self.fields['customer'].queryset = Customer.objects.filter(pk=instance.customer_id)
            self.fields['customer'].empty_value = []
            self.fields['customer'].empty_label = None
            self.fields['address'].queryset = Address.objects.filter(customer_id=instance.customer_id)
            self.fields['address'].empty_value = []
            self.fields['address'].empty_label = None

            if not instance.total_amount:
                self.fields.pop('total_amount')

            if instance.is_paid:
                self.fields['paid_time'].widget.attrs['readonly'] = True
            else:
                self.fields.pop('paid_time')

            if instance.ship_time:
                self.fields['ship_time'].widget.attrs['readonly'] = True
            else:
                self.fields.pop('ship_time')

            if instance.product_cost_aud is not None:
                if instance.shipping_fee is None:
                    instance.shipping_fee = 0
                cost_aud = '%s + %s = %s (%s)' % (instance.product_cost_aud, instance.shipping_fee,
                                                  instance.total_cost_aud, instance.total_cost_rmb)
                self.initial['cost_aud'] = cost_aud
                self.fields['cost_aud'].initial = cost_aud
                self.fields['cost_aud'].widget.attrs['readonly'] = True

                sell_rmb = '[%s] ' % instance.origin_sell_rmb if instance.origin_sell_rmb != instance.sell_price_rmb else ''
                sell_rmb += '%s - %s = %s' % (instance.sell_price_rmb, instance.total_cost_rmb,
                                              instance.profit_rmb)
                self.initial['sell_rmb'] = sell_rmb
                self.fields['sell_rmb'].initial = sell_rmb
                self.fields['sell_rmb'].widget.attrs['readonly'] = True
            else:
                self.fields.pop('status')
                self.fields.pop('cost_aud')
                self.fields.pop('sell_rmb')

            if instance.finish_time:
                self.fields['finish_time'].widget.attrs['readonly'] = True
            else:
                self.fields.pop('finish_time')

        if not instance.address:
            default_address = Customer.objects.filter(pk=instance.customer_id).first().primary_address
            self.initial['address'] = default_address
            self.fields['address'].initial = default_address


class OrderDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'address', 'is_paid', 'status', 'total_amount', 'product_cost_aud', 'product_cost_rmb',
                  'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb', 'origin_sell_rmb', 'sell_price_rmb',
                  'profit_rmb', 'finish_time']


# class OrderProductAddForm(NoManytoManyHintModelForm):
#     """ Add form for OrderProduct """
#
#     class Meta:
#         model = OrderProduct
#         fields = ['order', 'product', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud',
#                   'total_price_aud', 'store']


class OrderProductDetailForm(NoManytoManyHintModelForm):
    """ Detail form for OrderProduct """

    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud',
                  'total_price_aud', 'store']


# class OrderProductUpdateForm(NoManytoManyHintModelForm):
#     """ Update form for OrderProduct """
#
#     class Meta:
#         model = OrderProduct
#         fields = ['order', 'product', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud',
#                   'total_price_aud', 'store']



class OrderProductInlineForm(NoManytoManyHintModelForm):
    sum_price = forms.DecimalField(label=u'小计', required=False, help_text=u'小计',
                                   widget=forms.NumberInput(attrs={'class': 'form-control'}))
    product = forms.ModelChoiceField(label=u'产品', queryset=Product.objects.all(), required=False,
                                     widget=FormsetModelSelect2(url='product:product-autocomplete',
                                                                attrs={'data-placeholder': u'任意中英文名称...',
                                                                       'class': 'form-control'})
                                     )
    name = forms.CharField(label=u'名称', max_length=128, required=False, help_text=u'产品名称或备注(可选)',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    amount = forms.IntegerField(label=u'数量', min_value=1, required=False, help_text=u'数 量',
                                widget=forms.NumberInput(attrs={'class': 'form-control'}))
    sell_price_rmb = forms.DecimalField(label=u'售价', max_digits=8, decimal_places=2, required=False, help_text=u'单 价',
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cost_price_aud = forms.DecimalField(label=u'成本', max_digits=8, decimal_places=2, required=False, help_text=u'成 本',
                                        widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OrderProduct
        fields = ['product', 'order', 'name', 'amount', 'sell_price_rmb', 'sum_price', 'cost_price_aud', 'store']

    def __init__(self, *args, **kwargs):
        super(OrderProductInlineForm, self).__init__(*args, **kwargs)
        # self.fields['product'].queryset = Product.objects.all().order_by('brand__name_en', 'name_cn')
        self.fields['product'].widget.attrs['autocomplete'] = 'off'
        if 'store' in self.fields:
            self.fields['store'].widget.attrs['style'] = 'float:left;width:auto'
            self.fields['store'].widget.attrs['autocomplete'] = 'off'
        self.fields['order'].widget = forms.HiddenInput()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk and 'sum_price' in self.fields:
            self.fields['sum_price'].initial = instance.amount * instance.sell_price_rmb

    def clean_amount(self):
        return self.cleaned_data.get('amount') or 1


# OrderProductFormSet = modelformset_factory(OrderProduct, form=OrderProductInlineForm, extra=1)
OrderProductFormSet = inlineformset_factory(Order, OrderProduct, form=OrderProductInlineForm, extra=1)


class OrderProductFormForList(OrderProductInlineForm):
    class Meta:
        model = OrderProduct
        fields = ['product', 'order', 'name', 'amount', 'sell_price_rmb', 'cost_price_aud']

    def __init__(self, *args, **kwargs):
        super(OrderProductFormForList, self).__init__(*args, **kwargs)
        self.fields['sum_price'].widget = forms.HiddenInput()
