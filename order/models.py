from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from product.models import Product
from customer.models import Customer


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False, verbose_name=_('Product'))
    price_aud = models.DecimalField(_(u'price AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    price_rmb = models.DecimalField(_(u'price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    amount = models.IntegerField(_(u'amount'), default=0, blank=False, null=False, )
    total_price_aud = models.DecimalField(_(u'Total AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_rmb = models.DecimalField(_(u'Total RMB'), max_digits=8, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return '[P]%s X %s' % (self.product.name_cn, self.amount)


class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=False, null=False, verbose_name=_('Customer'))
    products = models.ManyToManyField(OrderProduct, blank=False, null=False, verbose_name=_('Product'))
    total_amount = models.IntegerField(_(u'amount'), default=0, blank=False, null=False)

    total_product_price_aud = models.DecimalField(_(u'Product price AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_product_price_rmb = models.DecimalField(_(u'Product price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)

    shipping_fee = models.DecimalField(_(u'shipping fee'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_aud = models.DecimalField(_(u'Total AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_rmb = models.DecimalField(_(u'Total RMB'), max_digits=8, decimal_places=2, blank=True, null=True)

    def __unicode__(self):
        return '[%s]%s' % (self.id, self.customer.name)





