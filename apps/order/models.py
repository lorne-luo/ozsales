from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from utils.enum import enum
from settings.settings import rate
from ..product.models import Product
from ..customer.models import Customer, Address
from ..store.models import Store

ORDER_STATUS = enum('CREATED', 'SHIPPING', 'DELIVERED', 'FINISHED')

ORDER_STATUS_CHOICES = (
    (ORDER_STATUS.CREATED, ORDER_STATUS.CREATED),
    (ORDER_STATUS.SHIPPING, ORDER_STATUS.SHIPPING),
    (ORDER_STATUS.DELIVERED, ORDER_STATUS.DELIVERED),
    (ORDER_STATUS.FINISHED, ORDER_STATUS.FINISHED),
)


@python_2_unicode_compatible
class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=False, null=False, verbose_name=_('customer'))
    address = models.ForeignKey(Address, blank=True, null=True, verbose_name=_('address'))
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS.CREATED,
                              verbose_name=_('status'))
    total_amount = models.IntegerField(_(u'Amount'), default=0, blank=False, null=False)
    product_cost_aud = models.DecimalField(_(u'Product Cost AUD'), max_digits=8, decimal_places=2, blank=True,
                                           null=True)
    product_cost_rmb = models.DecimalField(_(u'Product Cost RMB'), max_digits=8,
                                           decimal_places=2, blank=True, null=True)
    shipping_fee = models.DecimalField(_(u'Shipping Fee'), max_digits=8, decimal_places=2, blank=True, null=True)
    ship_time = models.DateTimeField(auto_now_add=False, editable=True, blank=True, null=True,
                                     verbose_name=_(u'Shipping Time'))
    total_cost_aud = models.DecimalField(_(u'Total Cost AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_cost_rmb = models.DecimalField(_(u'Total Cost RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    origin_sell_rmb = models.DecimalField(_(u'Origin Sell RMB'), max_digits=8, decimal_places=2, blank=True,
                                          null=True)
    sell_price_rmb = models.DecimalField(_(u'Sell Price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    profit_rmb = models.DecimalField(_(u'Profit RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    create_time = models.DateTimeField(_(u'Create Time'), auto_now_add=True, editable=False)
    finish_time = models.DateTimeField(_(u'Finish Time'), auto_now_add=False, editable=True)

    def __str__(self):
        return '[#%s]%s' % (self.id, self.customer.name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.product_cost_aud:
            self.product_cost_rmb = self.product_cost_aud * rate.aud_rmb_rate

        if self.shipping_fee:
            self.total_cost_aud = self.product_cost_aud + self.shipping_fee
            self.cost_rmb = self.total_cost_aud * rate.aud_rmb_rate

        if not self.sell_price_rmb:
            self.sell_price_rmb = self.origin_sell_rmb
        if self.sell_price_rmb < self.total_cost_rmb:
            self.sell_price_rmb = self.total_cost_rmb
        if self.sell_price_rmb and self.total_cost_rmb:
            self.profit_rmb = self.sell_price_rmb - self.total_cost_rmb

        return super(Order, self).save()

    def get_link(self):
        url = reverse('admin:%s_%s_change' % ('order', 'order'), args=[self.id])
        name = '[#%s]%s' % (self.id, self.customer.name)
        return u'<a href="%s">%s</a>' % (url, name)


    def update_price(self):
        self.total_amount = 0
        self.product_cost_aud = 0
        self.product_cost_rmb = 0
        self.origin_sell_rmb = 0
        self.shipping_fee = 0

        products = self.products.all()
        for p in products:
            self.total_amount += p.amount
            self.product_cost_aud += p.amount * p.cost_price_aud
            self.product_cost_rmb += self.product_cost_aud * rate.aud_rmb_rate
            self.origin_sell_rmb += p.sell_price_rmb * p.amount

        express_orders = self.express_orders.all()
        for ex_order in express_orders:
            self.ship_time = ex_order.create_time
            if ex_order.fee:
                self.shipping_fee += ex_order.fee

        self.total_cost_aud = self.product_cost_aud + self.shipping_fee
        self.total_cost_rmb = self.total_cost_aud * rate.aud_rmb_rate

        if not self.sell_price_rmb:
            self.sell_price_rmb = self.origin_sell_rmb
        if self.sell_price_rmb < self.total_cost_rmb:
            self.sell_price_rmb = self.total_cost_rmb
        self.profit_rmb = self.sell_price_rmb - self.total_cost_rmb

        self.save()

    def get_paid_button(self):
        if not self.is_paid:
            url = reverse('change-order-paid', kwargs={'order_id': self.id})
            return '<a href="%s">UNPAID</a>' % url
        return 'PAID'

    get_paid_button.allow_tags = True
    get_paid_button.short_description = 'Paid'

    def get_status_button(self):
        current_status = self.status
        next_status = ''
        express_orders = self.express_orders.all()
        if express_orders.count():
            for ex in express_orders:
                current_status = ex.get_tracking_link() + '<br/>' + current_status
        if self.status == ORDER_STATUS.CREATED:
            next_status = ORDER_STATUS.SHIPPING
        elif self.status == ORDER_STATUS.SHIPPING:
            next_status = ORDER_STATUS.DELIVERED
        elif self.status == ORDER_STATUS.DELIVERED:
            next_status = ORDER_STATUS.FINISHED
        else:
            return ORDER_STATUS.FINISHED

        url = reverse('change-order-status', kwargs={'order_id': self.id, 'status_str': next_status})
        btn = '%s => <a href="%s">%s</a>' % (current_status, url, next_status)
        return btn

    get_status_button.allow_tags = True
    get_status_button.short_description = 'Status'

    def get_id_upload(self):
        express_orders = self.express_orders.all()

        for ex_order in express_orders:
            if not ex_order.id_upload:
                return '<a target="_blank" href="%s"><b>UPLOAD</b></a>' % ex_order.carrier.website
        if not express_orders.count():
            return 'No Shipping'
        return 'DONE'

    get_id_upload.short_description = 'ID Upload'
    get_id_upload.allow_tags = True

    def get_customer_link(self):
        return self.customer.get_link()

    get_customer_link.allow_tags = True
    get_customer_link.short_description = 'Customer'


@python_2_unicode_compatible
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_('Order'), related_name='products')
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name=_('Product'))
    name = models.CharField(_(u'Name'), max_length=128, null=True, blank=True)
    amount = models.IntegerField(_(u'Amount'), default=0, blank=False, null=False, )
    sell_price_rmb = models.DecimalField(_(u'Sell Price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_rmb = models.DecimalField(_(u'Total RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    cost_price_aud = models.DecimalField(_(u'Cost Price AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_price_aud = models.DecimalField(_(u'Total AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    store = models.ForeignKey(Store, blank=True, null=True, verbose_name=_('Store'))
    create_time = models.DateTimeField(_(u'Create Time'), auto_now_add=True, editable=True)

    def __str__(self):
        return '%s X %s' % (self.name, self.amount)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.cost_price_aud:
            self.cost_price_aud = self.product.normal_price
        self.total_price_aud = self.cost_price_aud * self.amount

        if not self.sell_price_rmb:
            self.sell_price_rmb = self.product.safe_sell_price
        self.total_price_rmb = self.sell_price_rmb * self.amount

        if self.product and not self.name:
            self.name = self.product.get_name_cn()

        super(OrderProduct, self).save()


@receiver(post_save, sender=OrderProduct)
@receiver(post_delete, sender=OrderProduct)
def update_order_price(sender, instance=None, created=False, **kwargs):
    if instance.order.id:
        instance.order.update_price()
