from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from ..order.models import Order
from ..customer.models import Address


@python_2_unicode_compatible
class ExpressCarrier(models.Model):
    name_cn = models.CharField(_(u'name_cn'), max_length=50, null=False, blank=False)
    name_en = models.CharField(_(u'name_en'), max_length=50, null=True, blank=True)
    website = models.URLField(_(u'website'), blank=True, null=True)
    search_url = models.URLField(_(u'search url'), blank=True, null=True)
    rate = models.DecimalField(_(u'rate'), max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Express Carrier')
        verbose_name = _('Express Carrier')

    def __str__(self):
        return '[EC]%s' % self.name_en


@python_2_unicode_compatible
class ExpressOrder(models.Model):
    carrier = models.ForeignKey(ExpressCarrier, blank=False, null=False, verbose_name=_(u'carrier'))
    track_id = models.CharField(_(u'Track ID'), max_length=30, null=False, blank=False)
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_(u'order'), related_name='express_orders')
    fee = models.DecimalField(_(u'Shipping Fee'), max_digits=8, decimal_places=2,
                              blank=True, null=True)
    weight = models.DecimalField(_(u'Weight'), max_digits=8, decimal_places=2, blank=True,
                                 null=True)
    remarks = models.CharField(_('remarks'), max_length=128, null=True, blank=True)
    id_upload = models.BooleanField(_('ID uploaded'), default=False, null=False, blank=False)
    create_time = models.DateTimeField(_(u'Create Time'), auto_now_add=True, editable=True)

    class Meta:
        verbose_name_plural = _('Express Order')
        verbose_name = _('Express Order')

    def __str__(self):
        return '[%s]%s' % (self.carrier.name_cn, self.track_id)

    def get_track_url(self):
        if '%s' in self.carrier.search_url:
            return self.carrier.search_url % self.track_id
        else:
            return '%s?id=%s' % (self.carrier.search_url, self.track_id)

    def get_tracking_link(self):
        if self.track_id:
            return '<a target="_blank" href="%s">%s</a>' % (self.get_track_url(), self.track_id)
        else:
            return 'No Track ID'

    get_tracking_link.allow_tags = True
    get_tracking_link.short_description = 'Express Track'

    def get_order_link(self):
        return self.order.get_link()

    get_order_link.allow_tags = True
    get_order_link.short_description = 'Order'

    def get_address(self):
        return self.order.address


@receiver(post_save, sender=ExpressOrder)
@receiver(post_delete, sender=ExpressOrder)
def update_order_price(sender, instance=None, created=False, **kwargs):
    if instance.order.id:
        instance.order.update_price()

