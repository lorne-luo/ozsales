# coding=utf-8
import datetime
import time
import logging
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.http import urlquote, urlunquote
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from wechat_sdk import WechatConf, WechatBasic
from wechat_sdk.exceptions import OfficialAPIError
import conf as wx_conf

log = logging.getLogger(__name__)


@python_2_unicode_compatible
class WxApp(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    app_id = models.CharField(_(u'App ID'), max_length=128, null=False, blank=False)
    app_secret = models.CharField(_(u'App Secret'), max_length=128, null=False, blank=False)
    mch_id = models.CharField(_(u'MCH ID'), max_length=128, null=True, blank=True)   # 商户ID
    api_key = models.CharField(_(u'API Key'), max_length=128, null=True, blank=True) # 商户API密钥 只参与签名 不需要上传
    access_token = models.CharField(_(u'Access Token'), max_length=512, null=True, blank=True)
    token_expiry = models.DateTimeField(auto_now_add=False, editable=True, blank=True, null=True,
                                        verbose_name=_(u'Token Expiry'))
    jsapi_ticket = models.CharField(_(u'JsApi Ticket'), max_length=512, null=True, blank=True)
    ticket_expiry = models.DateTimeField(auto_now_add=False, editable=True, blank=True, null=True,
                                         verbose_name=_(u'Ticket Expiry'))
    update_at = models.DateTimeField(auto_now=True, editable=True, blank=True, null=True, verbose_name=_(u'Update At'))

    class Meta:
        verbose_name_plural = _('Weixin Apps')
        verbose_name = _('Weixin App')

    def __str__(self):
        return '%s' % self.name

    def is_token_expired(self):
        # expired return true
        if not isinstance(self.token_expiry, datetime.datetime):
            return True
        return self.token_expiry - timezone.now() < datetime.timedelta(seconds=60)

    def is_ticket_expired(self):
        if not isinstance(self.ticket_expiry, datetime.datetime):
            return True
        return self.ticket_expiry - timezone.now() < datetime.timedelta(seconds=60)

    def to_timestamp(self, dt):
        return time.mktime(dt.timetuple())

    def from_timestamp(self, ts):
        return datetime.datetime.fromtimestamp(ts, timezone.utc)

    @property
    def conf(self):
        conf_dict = {
            'appid': self.app_id,
            'appsecret': self.app_secret
        }
        if not self.is_token_expired():
            conf_dict.update({
                'access_token': self.access_token,
                'access_token_expires_at': self.to_timestamp(self.token_expiry)
            })

        if not self.is_ticket_expired():
            conf_dict.update({
                'jsapi_ticket': self.jsapi_ticket,
                'jsapi_ticket_expires_at': self.to_timestamp(self.ticket_expiry)
            })

        conf = WechatConf(**conf_dict)

        if self.is_token_expired():
            try:
                access_token_dict = conf.get_access_token()
                self.access_token = access_token_dict['access_token']
                self.token_expiry = self.from_timestamp(access_token_dict['access_token_expires_at'])
                log.info('Update token = %s, %s' % (self.access_token, self.token_expiry))
                self.save(update_fields=['access_token', 'token_expiry'])
            except OfficialAPIError as e:
                log.error('[get_access_token] code=%s, %s' % (e.errcode, e.errmsg))

        if self.is_ticket_expired():
            try:
                jsapi_ticket_dict = conf.get_jsapi_ticket()
                self.jsapi_ticket = jsapi_ticket_dict['jsapi_ticket']
                self.ticket_expiry = self.from_timestamp(jsapi_ticket_dict['jsapi_ticket_expires_at'])
                log.info('Update jsapi_ticket = %s, %s' % (self.jsapi_ticket, self.ticket_expiry))
                self.save(update_fields=['jsapi_ticket', 'ticket_expiry'])
            except OfficialAPIError as e:
                log.error('[get_jsapi_ticket] code=%s, %s' % (e.errcode, e.errmsg))

        return conf

    @property
    def api(self):
        return WechatBasic(conf=self.conf)

    def get_login_url(self, scope=wx_conf.SCOPE_USERINFO, state=''):
        url = reverse('weixin:auth', args=[self.name])
        template = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=http://%s%s&response_type=code&scope=%s&state=%s#wechat_redirect'
        return template % (self.app_id, wx_conf.BIND_DOMAIN, urlquote(url), scope, urlquote(state))
