# coding=utf-8
import logging
import re

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from pypinyin import Style

from core.auth_user.models import AuthUser
from core.aliyun.sms.service import send_cn_sms
from core.django.models import PinYinFieldModelMixin
from . import tracker as tracker
from ..member.models import Seller
from ..customer.models import Address, Customer
from ..order.models import Order

log = logging.getLogger(__name__)


class ExpressCarrierManager(models.Manager):
    DEFAULT_CACHE_KEY = 'QUERYSET_CACHE_DEFAULT_CARRIER'

    def clean_cache(self):
        log.info('[QUERYSET_CACHE] clean carriers.')
        cache.delete(self.DEFAULT_CACHE_KEY)

    def default(self):
        default_carrier = cache.get_or_set(
            self.DEFAULT_CACHE_KEY,
            super(ExpressCarrierManager, self).get_queryset().filter(seller__isnull=True),
            24 * 60 * 60)
        return default_carrier

    def all_for_seller(self, obj):
        if isinstance(obj, Seller):
            seller_id = obj.id
        elif isinstance(obj, AuthUser) and obj.is_seller:
            seller_id = obj.profile.id
        else:
            return ExpressCarrier.objects.none()

        default_carrier = self.default()
        qs = default_carrier | super(ExpressCarrierManager, self).get_queryset().filter(seller_id=seller_id)
        return self.order_by_usage_for_seller(qs, seller_id)

    def order_by_usage_for_seller(self, qs, seller_id):
        return qs.annotate(use_counter=models.Count(models.Case(
            models.When(expressorder__order__seller_id=seller_id, then=1),
            default=0,
            output_field=models.IntegerField()
        ))).order_by('-use_counter')

    def all_for_customer(self, obj):
        if isinstance(obj, Customer):
            customer_id = obj.id
        elif isinstance(obj, AuthUser) and obj.is_customer:
            customer_id = obj.profile.id
        else:
            return ExpressCarrier.objects.none()

        qs = super(ExpressCarrierManager, self).get_queryset()
        return self.order_by_usage_for_customer(qs, customer_id)

    def order_by_usage_for_customer(self, qs, customer_id):
        return qs.annotate(use_counter=models.Count(models.Case(
            models.When(expressorder__order__customer_id=customer_id, then=1),
            default=0,
            output_field=models.IntegerField()
        ))).order_by('-use_counter')


class ExpressCarrier(PinYinFieldModelMixin, models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    name_cn = models.CharField(_('中文名称'), max_length=255, blank=False, help_text='中文名称')
    name_en = models.CharField(_('英文名称'), max_length=255, blank=True, help_text='英文名称')
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    website = models.URLField(_('官网地址'), blank=True, help_text='官方网站地址')
    # page to track parcel
    search_url = models.URLField(_('查询网址'), blank=True, help_text='查询网页地址')
    # some carrier need post to track parcel
    post_search_url = models.URLField(_('查询提交网址'), blank=True, help_text='查询提交网址')
    id_upload_url = models.URLField(_('证件上传地址'), blank=True, help_text='证件上传地址')
    rate = models.DecimalField(_('费率'), max_digits=6, decimal_places=2, blank=True, null=True, help_text='每公斤费率')
    is_default = models.BooleanField('默认', default=False, help_text='是否默认')
    track_id_regex = models.CharField(_('单号正则'), max_length=512, blank=True, help_text='订单号正则表达式')

    objects = ExpressCarrierManager()
    pinyin_fields_conf = [
        ('name_cn', Style.NORMAL, False),
        ('name_cn', Style.FIRST_LETTER, False),
    ]

    class Meta:
        verbose_name_plural = _('Express Carrier')
        verbose_name = _('Express Carrier')

    def __str__(self):
        return '%s' % self.name_cn

    @staticmethod
    def get_incomplete_carrier_by_user(seller):
        # return first update required carrier
        return ExpressCarrier.objects.filter(seller=seller).filter(Q(website__isnull=True) | Q(website='')).first()

    def update_track(self, order):
        url = self.post_search_url or self.search_url or order.remarks
        if '%s' in url:
            url = url % order.track_id

        try:
            if not url or not url.startswith('http'):
                raise Exception('invalid url')

            if 'aupost' in self.website.lower():
                return None, None
            elif 'emms' in self.website.lower():
                return tracker.sfx_track(url)
            elif 'blueskyexpress' in self.website.lower():
                return tracker.bluesky_track(url)
            elif 'changjiang' in self.website.lower():
                return tracker.changjiang_track(url)
            elif 'au.transrush.com' in self.website.lower():
                return tracker.transrush_au_track(url)
            elif 'one-express' in self.website.lower():
                return tracker.one_express_track(url, order.track_id)
            elif 'arkexpress' in self.website.lower():
                return tracker.arkexpress_track(url)
            # todo more tracker
            else:
                return tracker.table_last_tr(url)
        except Exception as ex:
            log.info('%s track failed: %s' % (self.name_en, ex))
            return None, str(ex)

    def test_tracker(self):
        last_order = self.express_orders.filter(is_delivered=True).order_by('-create_time').first()
        last_order.test_tracker()

    @staticmethod
    def identify_carrier(track_id):
        for carrier in ExpressCarrier.objects.all():
            if carrier.track_id_regex:
                m = re.match(carrier.track_id_regex, track_id, re.IGNORECASE)
                if m and m.group():
                    return carrier
        return None

    @staticmethod
    def get_default_carrier():
        return ExpressCarrier.objects.filter(is_default=True).first()

    def save(self, *args, **kwargs):
        # default to update cache
        update_cache = kwargs.pop('update_cache', True)
        super(ExpressCarrier, self).save(*args, **kwargs)
        if update_cache:
            ExpressCarrier.objects.clean_cache()


class ExpressOrder(models.Model):
    carrier = models.ForeignKey(ExpressCarrier, blank=True, null=True, verbose_name=_('carrier'))
    track_id = models.CharField(_('Track ID'), max_length=30, null=False, blank=False, help_text='运单号')
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_('order'), related_name='express_orders')
    address = models.ForeignKey(Address, blank=True, null=True, verbose_name=_('address'))
    is_delivered = models.BooleanField(_('is delivered'), default=False, null=False, blank=False)
    last_track = models.CharField(_('last track'), max_length=512, null=True, blank=True)
    fee = models.DecimalField(_('Shipping Fee'), max_digits=8, decimal_places=2, default=0, blank=False, null=False,
                              help_text='运费')
    weight = models.DecimalField(_('Weight'), max_digits=8, decimal_places=2, blank=True, null=True, help_text='重量')
    id_upload = models.BooleanField(_('ID uploaded'), default=False, null=False, blank=False)
    remarks = models.CharField(_('Remarks'), max_length=128, null=True, blank=True)
    delivery_sms_sent = models.BooleanField(_('delivery sms'), default=False, null=False, blank=False)  # 寄达通知
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, editable=True)

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

        if not self.address and self.order and self.order.address:
            self.address = self.order.address

        if not self.pk:
            self.track_id = self.track_id.upper()
            if self.carrier and self.address:
                self.id_upload = ExpressOrder.objects.filter(carrier=self.carrier,
                                                             address=self.address,
                                                             id_upload=True).exists()
        return super(ExpressOrder, self).save()

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

    def get_address(self):
        return self.order.address

    def email_delivered(self):
        if self.is_delivered:
            link = reverse('order-detail-short', args=[self.order.customer.id, self.order.id])
            subject = '%s in %s 已寄达.' % (self, self.order)
            content = '%s in <a target="_blank" href="%s">%s</a> 已寄达.' % (self, link, self.order)

            self.order.seller.send_notification(subject, content)
            self.order.customer.send_email(subject, content)

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
            self.save(update_fields=['last_track', 'is_delivered'])

    def test_tracker(self):
        if self.is_delivered and self.carrier:
            delivered, last_info = self.carrier.update_track(self)
            if delivered is None:
                # deliverd is None = error
                log.info('%s tracker test failed. error = %s' % (self.carrier.name_en, last_info))


@receiver(post_save, sender=ExpressOrder)
def express_order_saved(sender, instance=None, created=False, **kwargs):
    if instance.order_id:
        instance.order.update_price(update_sell_price=True)


@receiver(post_delete, sender=ExpressOrder)
def express_order_deleted(sender, **kwargs):
    instance = kwargs['instance']
    if instance.order_id:
        instance.order.update_price(update_sell_price=True)


@receiver(post_save, sender=ExpressCarrier)
def update_default_carrier(sender, instance=None, created=False, **kwargs):
    if instance.is_default:
        ExpressCarrier.objects.exclude(id=instance.id).update(is_default=False)


@receiver(post_delete, sender=ExpressCarrier)
def express_carrier_deleted(sender, **kwargs):
    instance = kwargs['instance']
    if instance.seller is None:  # default carrier, clean cache
        ExpressCarrier.objects.clean_cache()


# ========================= carrier sub model ==================================

class DefaultCarrierManager(models.Manager):
    def get_queryset(self):
        return super(DefaultCarrierManager, self).get_queryset().filter(seller__isnull=True)


class DefaultCarrier(ExpressCarrier):
    objects = DefaultCarrierManager()

    class Meta:
        proxy = True


class CustomCarrierManager(models.Manager):
    def get_queryset(self):
        return super(CustomCarrierManager, self).get_queryset().filter(seller__isnull=False)

    def belong_to(self, obj):
        if isinstance(obj, Seller):
            seller_id = obj.id
        elif isinstance(obj, AuthUser) and obj.is_seller:
            seller_id = obj.profile.id
        else:
            return CustomCarrier.objects.none()

        return super(CustomCarrierManager, self).get_queryset().filter(seller_id=seller_id)


class CustomCarrier(ExpressCarrier):
    objects = CustomCarrierManager()

    class Meta:
        proxy = True
