# coding=utf-8
import logging
import re
from urllib.parse import urlparse

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from pypinyin import Style
from tldextract import tldextract

from core.django.models import PinYinFieldModelMixin
from . import tracker

log = logging.getLogger(__name__)


class CarrierTracker(PinYinFieldModelMixin, models.Model):
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
    need_id = models.BooleanField('需要身份证', default=False, help_text='是否需要身份证')
    id_upload_url = models.URLField(_('证件上传地址'), blank=True, help_text='证件上传地址')
    track_id_regex = models.CharField(_('单号正则'), max_length=512, blank=True, help_text='订单号正则表达式')
    last_track_id = models.CharField(_('最后单号'), max_length=512, blank=True)
    last_succeed_date = models.DateTimeField(_('最后成功'), auto_now_add=False, editable=True, blank=True, null=True)
    alias = models.CharField(_('别名'), max_length=255, blank=True)
    selector = models.CharField(_('CSS'), max_length=255, blank=True, default='table tr')
    item_index = models.IntegerField(_('顺序'), blank=True, default=-1)

    pinyin_fields_conf = [
        ('name_cn', Style.NORMAL, False),
        ('name_cn', Style.FIRST_LETTER, False),
    ]

    def __str__(self):
        return self.name_cn

    def save(self, *args, **kwargs):
        if not self.domain or self.domain not in self.website:
            parsed_uri = urlparse(self.website)
            ext = tldextract.extract(parsed_uri.netloc)
            self.domain = ext.registered_domain
        super(CarrierTracker, self).save(*args, **kwargs)

    def get_track_url(self, track_id):
        url = self.post_search_url or self.search_url
        if '%s' in url:
            url = url % track_id
        return url

    def update_track(self, track_id):
        url = self.get_track_url(track_id)
        if not url:
            return None, 'No track url provided.'

        try:
            if not url.startswith('http'):
                raise Exception('invalid url')
            if 'aupost' in self.website.lower():
                success, last_info = None, None
            elif 'au.transrush.com' in self.website.lower():
                success, last_info = tracker.transrush_au_track(url)
            elif 'one-express' in self.website.lower():
                success, last_info = tracker.one_express_track(url, track_id)
            elif 'ewe.com.au' in self.website.lower():
                success, last_info = tracker.ewe_track(url)
            elif 'aus-express.com' in self.website.lower():
                success, last_info = tracker.aus_express_track(url, track_id)
            # todo more tracker
            else:
                success, last_info = tracker.track_info(url, self.selector, self.item_index)

            if success:
                self.last_track_id = track_id
                self.last_succeed_date = timezone.now()
                self.save(update_fields=['last_track_id', 'last_succeed_date'])
            return success, last_info
        except Exception as ex:
            log.error('%s#%s track failed: %s' % (self.name_en, track_id, ex))
            return None, str(ex)

    # def test_tracker(self):
    #     delivered, last_info = self.update_track(self.last_track_id)
    #     if delivered is None:
    #         # deliverd is None = error
    #         log.info('%s tracker test failed. error = %s' % (self.name_en, last_info))

    @staticmethod
    def identify_carrier(track_id):
        for carrier in CarrierTracker.objects.all():
            if carrier.track_id_regex:
                m = re.match(carrier.track_id_regex, track_id, re.IGNORECASE)
                if m and m.group():
                    return carrier
        return None
