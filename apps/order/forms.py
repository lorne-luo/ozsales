# coding=utf-8
from django import forms
from django.contrib import admin
from django.forms.models import inlineformset_factory, BaseInlineFormSet, modelformset_factory
from dal import autocomplete
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from ..customer.models import Customer, Address
from ..product.models import Product
from models import Order, OrderProduct, ORDER_STATUS


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


class OrderAddForm(ModelForm):
    customer = forms.ModelChoiceField(
        queryset=Customer.objects.all(),
        widget=autocomplete.ModelSelect2(url='customer:customer-autocomplete',
                                         attrs={'data-placeholder': u'选择客户...'})
    )

    class Meta:
        model = Order
        fields = ['customer']

    def __init__(self, *args, **kwargs):
        super(OrderAddForm, self).__init__(*args, **kwargs)


class OrderUpdateForm(ModelForm):
    address = forms.ModelChoiceField(
        queryset=Address.objects.all(),
        widget=autocomplete.ModelSelect2(url='customer:address-autocomplete',
                                         forward=['customer'],
                                         attrs={'data-placeholder': u'选择地址...',})
    )

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


class OrderDetailForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'address', 'is_paid', 'status', 'total_amount', 'product_cost_aud', 'product_cost_rmb',
                  'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb', 'origin_sell_rmb', 'sell_price_rmb',
                  'profit_rmb', 'finish_time']


# class OrderProductAddForm(ModelForm):
#     """ Add form for OrderProduct """
#
#     class Meta:
#         model = OrderProduct
#         fields = ['order', 'product', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud',
#                   'total_price_aud', 'store']


class OrderProductDetailForm(ModelForm):
    """ Detail form for OrderProduct """

    class Meta:
        model = OrderProduct
        fields = ['order', 'product', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud',
                  'total_price_aud', 'store']


# class OrderProductUpdateForm(ModelForm):
#     """ Update form for OrderProduct """
#
#     class Meta:
#         model = OrderProduct
#         fields = ['order', 'product', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud',
#                   'total_price_aud', 'store']


class OrderProductInlineAddForm(ModelForm):
    sum_price = forms.DecimalField(required=False)

    class Meta:
        model = OrderProduct
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderProductInlineAddForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all().order_by('brand__name_en', 'name_cn')
        self.fields['product'].widget.attrs['class'] = 'form-control'
        self.fields['product'].widget.attrs['autocomplete'] = 'off'
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['sell_price_rmb'].widget.attrs['class'] = 'form-control'
        self.fields['sum_price'].widget.attrs['class'] = 'form-control'
        self.fields['cost_price_aud'].widget.attrs['class'] = 'form-control'
        self.fields['store'].widget.attrs['class'] = 'form-control'
        self.fields['store'].widget.attrs['style'] = 'float:left;width:auto'
        self.fields['store'].widget.attrs['autocomplete'] = 'off'
        self.fields['order'].widget = forms.HiddenInput()

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['sum_price'].initial = instance.amount * instance.sell_price_rmb


class OrderProductInlineForm(ModelForm):
    sum_price = forms.DecimalField(required=False)

    class Meta:
        model = OrderProduct
        fields = ['product', 'order', 'name', 'amount', 'sell_price_rmb', 'sum_price', 'cost_price_aud', 'store']

    def __init__(self, *args, **kwargs):
        super(OrderProductInlineForm, self).__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all().order_by('brand__name_en', 'name_cn')
        self.fields['product'].widget.attrs['autocomplete'] = 'off'
        self.fields['store'].widget.attrs['style'] = 'float:left;width:auto'
        self.fields['store'].widget.attrs['autocomplete'] = 'off'
        self.fields['order'].widget = forms.HiddenInput()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['sum_price'].initial = instance.amount * instance.sell_price_rmb


OrderProductFormSet = modelformset_factory(OrderProduct, form=OrderProductInlineForm,
                                           can_order=False, can_delete=False, extra=1)
