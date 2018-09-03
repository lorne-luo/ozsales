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


class DefaultCarrier(PinYinFieldModelMixin, models.Model):
    # todo find another way to store create by seller
    # seller = models.ForeignKey('member.Seller', blank=True, null=True)
    name_cn = models.CharField(_('中文名称'), max_length=255, blank=False, help_text='中文名称')
    name_en = models.CharField(_('英文名称'), max_length=255, blank=True, help_text='英文名称')
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    domain = models.CharField(_('domain'), max_length=512, blank=True, help_text='domain')
    website = models.URLField(_('官网地址'), blank=True, help_text='官方网站地址')
    # page to track parcel
    search_url = models.URLField(_('查询网址'), blank=True, help_text='查询网页地址')
    # some carrier need post to track parcel
    post_search_url = models.URLField(_('查询提交网址'), blank=True, help_text='查询提交网址')
    id_upload_url = models.URLField(_('证件上传地址'), blank=True, help_text='证件上传地址')
    rate = models.DecimalField(_('费率'), max_digits=6, decimal_places=2, blank=True, null=True, help_text='每公斤费率')
    is_default = models.BooleanField('默认', default=False, help_text='是否默认')
    track_id_regex = models.CharField(_('单号正则'), max_length=512, blank=True, help_text='订单号正则表达式')
    # latest_track_id = models.CharField(_('last track id'), max_length=512, blank=True)

    pinyin_fields_conf = [
        ('name_cn', Style.NORMAL, False),
        ('name_cn', Style.FIRST_LETTER, False),
    ]

    def __str__(self):
        return self.name_cn

    def update_track(self, track_id, url=None):
        url = self.post_search_url or self.search_url or url
        if not url:
            return None, 'No track url provided.'
        if '%s' in url:
            url = url % track_id

        try:
            if not url.startswith('http'):
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
                return tracker.one_express_track(url, track_id)
            elif 'arkexpress' in self.website.lower():
                return tracker.arkexpress_track(url)
            # todo more tracker
            else:
                return tracker.table_last_tr(url)
        except Exception as ex:
            log.info('%s track failed: %s' % (self.name_en, ex))
            return None, str(ex)

    # def test_tracker(self):
    #     delivered, last_info = self.update_track(self.latest_track_id)
    #     if delivered is None:
    #         # deliverd is None = error
    #         log.info('%s tracker test failed. error = %s' % (self.name_en, last_info))

    @staticmethod
    def identify_carrier(track_id):
        for carrier in DefaultCarrier.objects.all():
            if carrier.track_id_regex:
                m = re.match(carrier.track_id_regex, track_id, re.IGNORECASE)
                if m and m.group():
                    return carrier
        return None
