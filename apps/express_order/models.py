# coding=utf-8
import logging
import re

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from core.aliyun.sms.service import send_cn_sms
from ..express_carrier.models import ExpressCarrier

log = logging.getLogger(__name__)


class ExpressOrder(models.Model):
    carrier = models.ForeignKey(ExpressCarrier, blank=True, null=True, verbose_name=_('carrier'))
    track_id = models.CharField(_('Track ID'), max_length=30, null=False, blank=False, help_text='运单号')
    order = models.ForeignKey('order.Order', blank=False, null=False, verbose_name=_('order'),
                              related_name='express_orders')
    # address = models.ForeignKey('customer.Address', blank=True, null=True, verbose_name=_('address'))
    is_delivered = models.BooleanField(_('is delivered'), default=False, null=False, blank=False)
    last_track = models.CharField(_('last track'), max_length=512, null=True, blank=True)
    fee = models.DecimalField(_('Shipping Fee'), max_digits=8, decimal_places=2, default=0, blank=False, null=False,
                              help_text='运费')
    weight = models.DecimalField(_('Weight'), max_digits=8, decimal_places=2, blank=True, null=True, help_text='重量')
    id_upload = models.BooleanField(_('ID uploaded'), default=False, null=False, blank=False)
    remarks = models.CharField(_('Remarks'), max_length=128, null=True, blank=True)
    delivery_sms_sent = models.BooleanField(_('delivery sms'), default=False, null=False, blank=False)  # 寄达通知
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, editable=True)
    delivered_time = models.DateTimeField(_('寄达时间'), editable=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Express Order')
        verbose_name = _('Express Order')
        unique_together = ('carrier', 'track_id')

    def __str__(self):
        if self.carrier:
            return '[%s]%s' % (self.carrier.name_cn, self.track_id)
        else:
            return '[未知物流]%s' % (self.track_id)

    def identify_track_id(self):
        if self.carrier and self.carrier.track_id_regex:
            # check track_id match current regex or not
            m = re.match(self.carrier.track_id_regex, self.track_id, re.IGNORECASE)
            if not m:
                msg = '%s not match %s regex=%s' % (self.track_id, self.carrier.name_cn, self.carrier.track_id_regex)
                log.info('[AUTO_TRACK_ID.NEW_FORMAT_FOUND] %s' % msg)
        elif not self.carrier and self.track_id:
            self.carrier = ExpressCarrier.identify_carrier(self.track_id) or ExpressCarrier.get_default_carrier()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.identify_track_id()

        if not self.pk:
            self.track_id = self.track_id.upper()
            if self.carrier and self.address:
                self.id_upload = ExpressOrder.objects.filter(carrier=self.carrier,
                                                             address=self.address,
                                                             id_upload=True).exists()
        return super(ExpressOrder, self).save(force_insert, force_update, using, update_fields)

    def get_track_url(self):
        if not self.carrier:
            return '#'
        if self.remarks and self.remarks.startswith('http'):
            return self.remarks
        elif '%s' in self.carrier.search_url:
            return self.carrier.search_url % self.track_id
        else:
            return None

    def get_tracking_link(self):
        if self.id_upload:
            return '<a target="_blank" href="%s">%s</a>' % (self.get_track_url(), self.track_id)
        elif self.carrier:
            return '<a target="_blank" href="%s"><i><b>%s</b></i></a>' % (
                self.carrier.id_upload_url or self.get_track_url(), self.track_id)
        else:
            return self.track_id

    get_tracking_link.allow_tags = True
    get_tracking_link.short_description = 'Express Track'

    def get_order_link(self):
        return self.order.get_link()

    get_order_link.allow_tags = True
    get_order_link.short_description = 'Order'

    @property
    def address(self):
        if self.order:
            return self.order.address
        return None

    def sms_delivered(self):
        mobile = self.order.get_mobile()
        if not mobile or self.delivery_sms_sent:
            return

        bz_id = 'ExpressOrder#%s-delivered' % self.track_id
        url = reverse('order-detail-short', kwargs={'customer_id': self.order.customer.id, 'pk': self.order.id})
        data = "{\"track_id\":\"%s\", \"url\":\"%s\"}" % (self.track_id, url)
        success, detail = send_cn_sms(bz_id, mobile, settings.PACKAGE_DELIVERED_TEMPLATE, data)
        if success:
            self.delivery_sms_sent = True
            self.save(update_fields=['delivery_sms_sent'])

    def update_track(self):
        if self.is_delivered or not self.carrier:
            return

        if self.create_time > timezone.now() - relativedelta(days=3):
            return  # send less than 3 days, skip

        delivered, last_info = self.carrier.update_track(self)
        if delivered in [True, False]:
            self.is_delivered = delivered
            self.last_track = last_info[:512]
            if delivered:
                self.delivered_time = timezone.now()
            self.save(update_fields=['last_track', 'is_delivered', 'delivered_time'])

    def test_tracker(self):
        if self.is_delivered and self.carrier:
            delivered, last_info = self.carrier.update_track(self)
            if delivered is None:
                # deliverd is None = error
                log.info('%s tracker test failed. error = %s' % (self.carrier.name_en, last_info))

    @property
    def shipping_days(self):
        if self.delivered_time and self.create_time:
            diff = self.delivered_time - self.create_time
            return diff.days
        return -1


@receiver(post_save, sender=ExpressOrder)
def express_order_saved(sender, instance=None, created=False, **kwargs):
    if instance.order_id:
        instance.order.update_price(update_sell_price=True)


@receiver(post_delete, sender=ExpressOrder)
def express_order_deleted(sender, **kwargs):
    instance = kwargs['instance']
    if instance.order_id:
        instance.order.update_price(update_sell_price=True)
