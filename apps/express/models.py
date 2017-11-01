import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, pre_save
import apps.express.tracker as tracker
from ..order.models import Order
from ..customer.models import Address

log = logging.getLogger(__name__)


@python_2_unicode_compatible
class ExpressCarrier(models.Model):
    name_cn = models.CharField(_('name_cn'), max_length=50, null=False, blank=False)
    name_en = models.CharField(_('name_en'), max_length=50, null=True, blank=True)
    website = models.URLField(_('Website'), blank=True, null=True)
    search_url = models.URLField(_('Search url'), blank=True, null=True)
    rate = models.DecimalField(_('Rate'), max_digits=6, decimal_places=2, blank=True, null=True)
    is_default = models.BooleanField('Default', default=False)

    class Meta:
        verbose_name_plural = _('Express Carrier')
        verbose_name = _('Express Carrier')

    def __str__(self):
        return '%s' % self.name_cn

    def update_track(self, url):
        try:
            if 'aupost' in self.website.lower():
                return None, None
            elif 'emms' in self.website.lower():
                return tracker.sfx_track(url)
            elif 'changjiang' in self.website.lower():
                return tracker.changjiang_track(url)
            # todo more tracker
            else:
                return tracker.table_last_tr(url)
        except Exception as ex:
            log.info('%s track failed: %s' % (self.name_en, ex))
            return None, str(ex)

    def test_tracker(self):
        last_order = self.express_orders.filter(is_delivered=True).order_by('-create_time').first()
        last_order.test_tracker()


@python_2_unicode_compatible
class ExpressOrder(models.Model):
    carrier = models.ForeignKey(ExpressCarrier, blank=True, null=True, verbose_name=_('carrier'))
    track_id = models.CharField(_('Track ID'), max_length=30, null=False, blank=False)
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_('order'), related_name='express_orders')
    address = models.ForeignKey(Address, blank=True, null=True, verbose_name=_('address'))
    is_delivered = models.BooleanField(_('is delivered'), default=False, null=False, blank=False)
    last_track = models.CharField(_('last track'), max_length=512, null=True, blank=True)
    fee = models.DecimalField(_('Shipping Fee'), max_digits=8, decimal_places=2,
                              blank=True, null=True)
    weight = models.DecimalField(_('Weight'), max_digits=8, decimal_places=2, blank=True,
                                 null=True)
    id_upload = models.BooleanField(_('ID uploaded'), default=False, null=False, blank=False)
    remarks = models.CharField(_('Remarks'), max_length=128, null=True, blank=True)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, editable=True)

    class Meta:
        verbose_name_plural = _('Express Order')
        verbose_name = _('Express Order')
        unique_together = ('carrier', 'track_id')

    def __str__(self):
        return '[%s]%s' % (self.carrier.name_cn, self.track_id)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.carrier:
            self.carrier = ExpressCarrier.objects.filter(is_default=True).first()

        if not self.address and self.order and self.order.address:
            self.address = self.order.address

        if not self.pk:
            self.track_id = self.track_id.upper()
            self.id_upload = ExpressOrder.objects.filter(carrier=self.carrier,
                                                         address=self.address,
                                                         id_upload=True).exists()
        return super(ExpressOrder, self).save()

    def get_track_url(self):
        if self.remarks and self.remarks.startswith('http'):
            return self.remarks
        elif '%s' in self.carrier.search_url:
            return self.carrier.search_url % self.track_id
        else:
            return None

    def get_tracking_link(self):
        if self.id_upload:
            return '<a target="_blank" href="%s">%s</a>' % (self.get_track_url(), self.track_id)
        else:
            return '<a target="_blank" href="%s"><i><b>%s</b></i></a>' % (self.get_track_url(), self.track_id)

    get_tracking_link.allow_tags = True
    get_tracking_link.short_description = 'Express Track'

    def get_order_link(self):
        return self.order.get_link()

    get_order_link.allow_tags = True
    get_order_link.short_description = 'Order'

    def get_address(self):
        return self.order.address

    def update_track(self):
        if not self.is_delivered:
            delivered, last_info = self.carrier.update_track(self.get_track_url())
            if delivered is not None:
                self.is_delivered = delivered
                self.last_track = last_info[:512]
                self.save(update_fields=['last_track', 'last_track'])

    def test_tracker(self):
        if self.is_delivered:
            delivered, last_info = self.carrier.update_track(self.get_track_url())
            if not delivered:
                log.info('%s tracker test failed. error = %s' % (self.carrier.name_en, last_info))


@receiver(post_save, sender=ExpressOrder)
def update_order_price(sender, instance=None, created=False, **kwargs):
    if instance.order and instance.order.id:
        instance.order.update_price()


@receiver(pre_save, sender=ExpressCarrier)
def update_default_carrier(sender, instance=None, created=False, **kwargs):
    if instance.is_default:
        ExpressCarrier.objects.all().update(is_default=False)
