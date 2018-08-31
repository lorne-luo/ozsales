# coding=utf-8
import logging
import re

from django.core.cache import cache
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from pypinyin import Style

from core.django.models import PinYinFieldModelMixin
from . import tracker

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

    def order_by_usage_for_seller(self, qs, seller_id):
        return qs.annotate(use_counter=models.Count(models.Case(
            models.When(expressorder__order__seller_id=seller_id, then=1),
            default=0,
            output_field=models.IntegerField()
        ))).order_by('-use_counter')

    def order_by_usage_for_customer(self, qs, customer_id):
        return qs.annotate(use_counter=models.Count(models.Case(
            models.When(expressorder__order__customer_id=customer_id, then=1),
            default=0,
            output_field=models.IntegerField()
        ))).order_by('-use_counter')


class ExpressCarrier(PinYinFieldModelMixin, models.Model):
    #todo find another way to store create by seller
    # seller = models.ForeignKey('member.Seller', blank=True, null=True)
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


@receiver(post_save, sender=ExpressCarrier)
def update_default_carrier(sender, instance=None, created=False, **kwargs):
    if instance.is_default:
        ExpressCarrier.objects.exclude(id=instance.id).update(is_default=False)


@receiver(post_delete, sender=ExpressCarrier)
def express_carrier_deleted(sender, **kwargs):
    instance = kwargs['instance']
    if instance.seller is None:  # default carrier, clean cache
        ExpressCarrier.objects.clean_cache()
