from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible

from utils.enum import enum
from settings.settings import RATE
from ..product.models import Product
from ..customer.models import Customer, Address
from ..store.models import Store

ORDER_STATUS = enum('CREATED', 'PAID', 'SHIPPED', 'DELIVERED', 'FINISHED')

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS.CREATED, ORDER_STATUS.CREATED),
    (ORDER_STATUS.PAID, ORDER_STATUS.PAID),
    (ORDER_STATUS.SHIPPED, ORDER_STATUS.SHIPPED),
    (ORDER_STATUS.DELIVERED, ORDER_STATUS.DELIVERED),
    # (ORDER_STATUS.RECEIVED, ORDER_STATUS.RECEIVED),
    (ORDER_STATUS.FINISHED, ORDER_STATUS.FINISHED),
)


@python_2_unicode_compatible
class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=False, null=False, verbose_name=_('customer'))
    address = models.ForeignKey(Address, blank=True, null=True, verbose_name=_('address'))
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS.CREATED,
                              verbose_name=_('status'))
    total_amount = models.IntegerField(_(u'amount'), default=0, blank=False, null=False)
    product_cost_aud = models.DecimalField(_(u'Product cost AUD'), max_digits=8, decimal_places=2, blank=True,
                                           null=True)
    product_cost_rmb = models.DecimalField(_(u'Product cost RMB'), max_digits=8,
                                           decimal_places=2, blank=True, null=True)
    shipping_fee = models.DecimalField(_(u'shipping fee'), max_digits=8, decimal_places=2, blank=True, null=True)
    ship_time = models.DateTimeField(auto_now_add=False, editable=True, blank=True, null=True,
                                     verbose_name=_(u'ship time'))
    total_cost_aud = models.DecimalField(_(u'Total Cost AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_cost_rmb = models.DecimalField(_(u'Total Cost RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price = models.DecimalField(_(u'price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    profit_rmb = models.DecimalField(_(u'profit RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    create_time = models.DateTimeField(_(u'create time'), auto_now_add=True, editable=True)

    def __str__(self):
        return '[%s]%s' % (self.id, self.customer.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.product_cost_aud:
            self.product_cost_rmb = self.product_cost_aud * RATE

        if self.shipping_fee:
            self.total_cost_aud = self.product_cost_aud + self.shipping_fee
            self.cost_rmb = self.total_cost_aud * RATE

        if self.total_cost_aud and self.sell_price:
            self.profit_rmb = self.sell_price - self.total_cost_aud * RATE

        if self.id:
            self.sum_cost()

        return super(Order, self).save()

    def sum_cost(self):
        self.total_amount = 0
        self.product_cost_aud = 0
        self.product_cost_rmb = 0

        products = self.products.all()
        for p in products:
            self.total_amount += p.amount
            self.product_cost_aud += p.amount * p.cost_price_aud
            self.product_cost_rmb += p.amount * p.sell_price_rmb

    def sum_cost_save(self):
        self.sum_cost()
        self.save()

    def status_button(self):
        next_status = ''
        if self.status == ORDER_STATUS.CREATED:
            next_status = ORDER_STATUS.PAID
        elif self.status == ORDER_STATUS.PAID:
            next_status = ORDER_STATUS.SHIPPED
        elif self.status == ORDER_STATUS.SHIPPED:
            next_status = ORDER_STATUS.DELIVERED
        elif self.status == ORDER_STATUS.DELIVERED:
            next_status = ORDER_STATUS.FINISHED
        else:
            return ORDER_STATUS.FINISHED

        url = reverse('change-order-status', kwargs={'order_id': self.id, 'status_str': next_status})
        btn = '%s => <a href="%s">%s</a>' % (self.status, url, next_status)
        return btn

    status_button.allow_tags = True
    status_button.short_description = 'Status'


@python_2_unicode_compatible
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_('Order'), related_name='products')
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name=_('Product'))
    name = models.CharField(_(u'name'), max_length=128, null=True, blank=True)
    cost_price_aud = models.DecimalField(_(u'cost price AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price_rmb = models.DecimalField(_(u'sell price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    amount = models.IntegerField(_(u'amount'), default=0, blank=False, null=False, )
    store = models.ForeignKey(Store, blank=True, null=True, verbose_name=_('Store'))
    total_price_aud = models.DecimalField(_(u'Total AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_rmb = models.DecimalField(_(u'Total RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    create_time = models.DateTimeField(_(u'create time'), auto_now_add=True, editable=True)

    def __str__(self):
        return '[OP]%s X %s' % (self.product.name_cn, self.amount)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.total_price_aud = self.cost_price_aud * self.amount
        self.total_price_rmb = self.sell_price_rmb * self.amount

        if self.product and not self.name:
            self.name = self.product.get_name_cn()

        super(OrderProduct, self).save()
        self.order.sum_cost_save()



