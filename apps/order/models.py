from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from ..product.models import Product
from ..customer.models import Customer, Address
from django.utils.encoding import python_2_unicode_compatible
from utils.enum import enum

ORDER_STATUS = enum('CREATED', 'PURCHASED', 'DELIVERED', 'RECEIVED', 'FINISHED')

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS.CREATED, ORDER_STATUS.CREATED),
    (ORDER_STATUS.PURCHASED, ORDER_STATUS.PURCHASED),
    (ORDER_STATUS.DELIVERED, ORDER_STATUS.DELIVERED),
    (ORDER_STATUS.RECEIVED, ORDER_STATUS.RECEIVED),
    (ORDER_STATUS.FINISHED, ORDER_STATUS.FINISHED),
)


@python_2_unicode_compatible
class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=False, null=False, verbose_name=_('Customer'))
    address = models.ForeignKey(Address, blank=False, null=False, verbose_name=_('Address'))
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS.CREATED)

    total_amount = models.IntegerField(_(u'amount'), default=0, blank=False, null=False)

    total_product_price_aud = models.DecimalField(_(u'Product price AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_product_price_rmb = models.DecimalField(_(u'Product price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)

    shipping_fee = models.DecimalField(_(u'shipping fee'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_aud = models.DecimalField(_(u'Total AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_rmb = models.DecimalField(_(u'Total RMB'), max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '[%s]%s' % (self.id, self.customer.name)


@python_2_unicode_compatible
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_('Order'))
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name=_('Product'))
    price_aud = models.DecimalField(_(u'price AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    price_rmb = models.DecimalField(_(u'price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    amount = models.IntegerField(_(u'amount'), default=0, blank=False, null=False, )
    total_price_aud = models.DecimalField(_(u'Total AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_rmb = models.DecimalField(_(u'Total RMB'), max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '[OP]%s X %s' % (self.product.name_cn, self.amount)



