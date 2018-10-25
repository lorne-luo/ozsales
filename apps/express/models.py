# coding=utf-8
import logging
import re
import tldextract
from urllib.parse import urlparse

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from pypinyin import Style

from core.aliyun.sms.service import send_cn_sms
from core.django.models import PinYinFieldModelMixin, TenantModelMixin

log = logging.getLogger(__name__)


class ExpressCarrier(PinYinFieldModelMixin, TenantModelMixin, models.Model):
    name_cn = models.CharField(_('中文名称'), max_length=255, blank=False, help_text='中文名称')
    name_en = models.CharField(_('英文名称'), max_length=255, blank=True, help_text='英文名称')
    website = models.URLField(_('官网地址'), blank=True, help_text='官方网站地址')
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    is_default = models.BooleanField('默认', default=False, help_text='是否默认')
    tracker = models.OneToOneField('carrier_tracker.CarrierTracker', blank=True, null=True)

    pinyin_fields_conf = [
        ('name_cn', Style.NORMAL, False),
        ('name_cn', Style.FIRST_LETTER, False),
    ]

    def __str__(self):
        return self.name_cn or self.name_en

    @property
    def track_id_regex(self):
        return self.tracker.track_id_regex if self.tracker else None

    @property
    def id_upload_url(self):
        return self.tracker.id_upload_url if self.tracker else None

    @property
    def post_search_url(self):
        return self.tracker.post_search_url if self.tracker else None

    @property
    def search_url(self):
        return self.tracker.search_url if self.tracker else None

    @property
    def domain(self):
        return self.tracker.domain if self.tracker else None

    @staticmethod
    def get_incomplete_carrier():
        # return first update required carrier
        return ExpressCarrier.objects.filter(Q(website__isnull=True) | Q(website='')).first()

    @staticmethod
    def get_default_carrier():
        return ExpressCarrier.objects.filter(is_default=True).first()

    @staticmethod
    def identify_carrier(track_id):
        for carrier in ExpressCarrier.objects.all():
            if carrier.track_id_regex:
                m = re.match(carrier.track_id_regex, track_id, re.IGNORECASE)
                if m and m.group():
                    return carrier
        return None

    def update_track(self, track_id, url=None):
        if self.tracker:
            return self.tracker.update_track(track_id, url)
        return None, 'No tracker linked for %s' % self


class ExpressOrder(TenantModelMixin, models.Model):
    carrier = models.ForeignKey(ExpressCarrier, blank=True, null=True, verbose_name=_('carrier'))
    track_id = models.CharField(_('Track ID'), max_length=30, null=False, blank=False, help_text='运单号')
    order = models.ForeignKey('order.Order', blank=False, null=False, verbose_name=_('order'),
                              related_name='express_orders')
    address = models.ForeignKey('customer.Address', blank=True, null=True, verbose_name=_('address'))
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
        ordering = ["create_time"]

    def __str__(self):
        if self.carrier:
            return '[%s]%s' % (self.carrier.name_cn, self.track_id)
        else:
            return '[未知物流]%s' % self.track_id

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

        if not self.id and not self.address:
            self.address = self.order.address

        if self._state.adding:
            self.track_id = self.track_id.upper()
            if self.carrier and self.address and not self.id_upload:
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

    def sms_delivered(self):
        mobile = self.order.get_customer_mobile()
        if not mobile or self.delivery_sms_sent:
            return

        bz_id = 'ExpressOrder#%s-delivered' % self.track_id
        data = "{\"track_id\":\"%s\", \"url\":\"%s\"}" % (self.track_id, self.order.public_url)
        success, detail = send_cn_sms(bz_id, mobile, settings.PACKAGE_DELIVERED_TEMPLATE, data)
        if success:
            self.delivery_sms_sent = True
            self.save(update_fields=['delivery_sms_sent'])

    def update_track(self):
        if self.is_delivered or not self.carrier:
            return

        if self.create_time > timezone.now() - relativedelta(days=3):
            return  # send less than 3 days, skip

        delivered, last_info = self.carrier.update_track(self.track_id)
        if delivered in [True, False]:
            self.is_delivered = delivered
            self.last_track = last_info[:512]
            if delivered:
                self.delivered_time = timezone.now()
            self.save(update_fields=['last_track', 'is_delivered', 'delivered_time'])

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
