# coding=utf-8
import datetime
import time
import logging
import conf as wx_conf
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.http import urlquote, urlunquote
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from wechat_sdk import WechatConf, WechatBasic
from wechat_sdk.exceptions import OfficialAPIError
from weixin.login import WeixinLogin
from weixin.mp import WeixinMP
from weixin.pay import WeixinPay, WeixinError, WeixinPayError

log = logging.getLogger(__name__)


@python_2_unicode_compatible
class WxApp(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    app_id = models.CharField(_(u'App ID'), max_length=128, null=False, blank=False)
    app_secret = models.CharField(_(u'App Secret'), max_length=128, null=False, blank=False)
    mch_id = models.CharField(_(u'MCH ID'), max_length=128, null=True, blank=True)  # 商户ID
    mch_key = models.CharField(_(u'MCH Key'), max_length=128, null=True, blank=True)  # 商户API密钥 只参与签名 不需要上传
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

    @property
    def is_token_expired(self):
        # expired return true
        if not isinstance(self.token_expiry, datetime.datetime):
            return True
        return self.token_expiry - timezone.now() < datetime.timedelta(seconds=60)

    @property
    def is_ticket_expired(self):
        if not isinstance(self.ticket_expiry, datetime.datetime):
            return True
        return self.ticket_expiry - timezone.now() < datetime.timedelta(seconds=60)

    def get_access_token(self):
        if self.is_token_expired:
            try:
                conf = WechatConf(appid=self.app_id, appsecret=self.app_secret)
                access_token_dict = conf.get_access_token()
                self.access_token = access_token_dict['access_token']
                self.token_expiry = self.from_timestamp(access_token_dict['access_token_expires_at'])
                self.save(update_fields=['access_token', 'token_expiry'])
                log.info('Update token = %s, %s' % (self.access_token, self.token_expiry))
            except OfficialAPIError as e:
                log.error('[get_access_token] code=%s, %s' % (e.errcode, e.errmsg))

        return self.access_token

    def get_jsapi_ticket(self):
        if self.is_ticket_expired:
            try:
                conf = WechatConf(appid=self.app_id, appsecret=self.app_secret)
                jsapi_ticket_dict = conf.get_jsapi_ticket()
                self.jsapi_ticket = jsapi_ticket_dict['jsapi_ticket']
                self.ticket_expiry = self.from_timestamp(jsapi_ticket_dict['jsapi_ticket_expires_at'])
                self.save(update_fields=['jsapi_ticket', 'ticket_expiry'])
                log.info('Update jsapi_ticket = %s, %s' % (self.jsapi_ticket, self.ticket_expiry))
            except OfficialAPIError as e:
                log.error('[get_jsapi_ticket] code=%s, %s' % (e.errcode, e.errmsg))

        return self.jsapi_ticket

    def to_timestamp(self, dt):
        return time.mktime(dt.timetuple())

    def from_timestamp(self, ts):
        return datetime.datetime.fromtimestamp(ts, timezone.utc)

    @property
    def conf(self):
        conf_dict = {
            'appid': self.app_id,
            'appsecret': self.app_secret,
            'access_token': self.get_access_token(),
            'access_token_expires_at': self.to_timestamp(self.token_expiry),
            'jsapi_ticket': self.get_jsapi_ticket,
            'jsapi_ticket_expires_at': self.to_timestamp(self.ticket_expiry)
        }

        return WechatConf(**conf_dict)

    @property
    def api(self):
        return WechatBasic(conf=self.conf)

    @property
    def mp(self):
        return WeixinMP(self.app_id, self.app_secret,
                        '/tmp/.%s_access_token' % self.name,
                        '/tmp/.%s_jsapi_ticket' % self.name)

    @property
    def pay(self):
        url = reverse('weixin:pay_notify', args=[self.name])
        full_url = 'http://%s%s' % (wx_conf.BIND_DOMAIN, url)
        pay = WeixinPay(self.app_id, self.mch_id, self.mch_key, full_url)
        return pay

    def get_login_url(self, scope=wx_conf.SCOPE_USERINFO, state=''):
        url = reverse('weixin:auth', args=[self.name])
        full_url = 'http://%s%s' % (wx_conf.BIND_DOMAIN, url)
        wx_login = WeixinLogin(self.app_id, self.app_secret)
        return wx_login.authorize(full_url, scope, state)


class WxReturnCode(object):
    SUCCESS = 'SUCCESS'
    FAIL = 'FAIL'

    CHOICES = (
        (FAIL, FAIL),
        (SUCCESS, SUCCESS),
    )


class PaymentStatus(object):
    SUCCESS = 'SUCCESS'
    REFUND = 'REFUND'
    NOTPAY = 'NOTPAY'
    CLOSED = 'CLOSED'
    REVOKED = 'REVOKED'
    USERPAYING = 'USERPAYING'  # 用户支付中
    PAYERROR = 'PAYERROR'  # 支付失败

    CHOICES = (
        (SUCCESS, '支付成功'),
        (REFUND, '已退款'),
        (NOTPAY, '未付款'),
        (CLOSED, '支付关闭'),
        (REVOKED, '已撤销'),
        (USERPAYING, '支付中'),
        (PAYERROR, '支付失败'),
    )


class WxOrder(models.Model):
    order = models.OneToOneField('order.Order')
    return_code = models.CharField(max_length=16, blank=True, null=True,
                                   choices=WxReturnCode.CHOICES)  # 返回状态码 SUCCESS/FAIL
    return_msg = models.CharField(max_length=128, blank=True, null=True)  # 返回信息，如非空，为错误原因
    result_code = models.CharField(max_length=16, blank=True, null=True,
                                   choices=WxReturnCode.CHOICES)  # 业务结果	 SUCCESS/FAIL
    appid = models.CharField(max_length=32, blank=True, null=True)  # 公众账号ID
    mch_id = models.CharField(max_length=32, blank=True, null=True)  # 商户号
    device_info = models.CharField(max_length=32, blank=True, null=True)  # 设备号
    nonce_str = models.CharField(max_length=32, blank=True, null=True)  # 返回的随机字符串
    sign = models.CharField(max_length=32, blank=True, null=True)  # 微信返回的签名值
    err_code = models.CharField(max_length=32, blank=True, null=True)  # 错误代码
    err_code_des = models.CharField(max_length=128, blank=True, null=True)  # 错误信息描述
    trade_type = models.CharField(max_length=16, blank=True, null=True)  # 交易类型
    # 预支付交易会话标识,微信生成的预支付回话标识，用于后续接口调用中使用，该值有效期为2小时
    prepay_id = models.CharField(max_length=64, blank=True, null=True)  # 预支付交易会话标识
    xml_response = models.TextField(blank=True, null=True)  # unifiedorder统一下单接口返回的原始xml

    @property
    def is_success(self):
        if self.return_code == WxReturnCode.SUCCESS and self.result_code == WxReturnCode.SUCCESS and self.prepay_id:
            return True
        else:
            return False

    def get_jsapi(self):
        app = WxApp.objects.get(app_id=self.appid)
        # fixme self.xml_response format
        package = "prepay_id={0}".format(self.prepay_id)
        timestamp = str(int(time.time()))
        nonce_str = app.pay.nonce_str
        raw = dict(appId=app.pay.app_id, timeStamp=timestamp,
                   nonceStr=nonce_str, package=package, signType="MD5")
        sign = app.pay.sign(raw)
        jsapi_dict = dict(package=package, appId=app.pay.app_id,
                          timeStamp=timestamp, nonceStr=nonce_str, sign=sign)
        return jsapi_dict


class WxPayment(models.Model):
    # https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2
    order = models.OneToOneField('order.Order')
    transaction_id = models.CharField(max_length=32, blank=True, null=True)  # 微信支付订单号
    return_code = models.CharField(max_length=16, blank=True, null=True,
                                   choices=WxReturnCode.CHOICES)  # 返回状态码 SUCCESS/FAIL
    return_msg = models.CharField(max_length=128, blank=True, null=True)  # 返回信息，如非空，为错误原因
    result_code = models.CharField(max_length=16, blank=True, null=True,
                                   choices=WxReturnCode.CHOICES)  # 业务结果	 SUCCESS/FAIL
    appid = models.CharField(max_length=32, blank=True, null=True)  # 公众账号ID
    mch_id = models.CharField(max_length=32, blank=True, null=True)  # 商户号
    device_info = models.CharField(max_length=32, blank=True, null=True)  # 设备号
    nonce_str = models.CharField(max_length=32, blank=True, null=True)  # 返回的随机字符串
    # 微信返回的签名值 https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_3
    sign = models.CharField(max_length=32, blank=True, null=True)
    err_code = models.CharField(max_length=32, blank=True, null=True)  # 错误代码
    err_code_des = models.CharField(max_length=128, blank=True, null=True)  # 错误信息描述
    openid = models.CharField(max_length=128, blank=True, null=True)
    is_subscribe = models.BooleanField(blank=False, null=False, default=False)  # 用户是否关注公众账号
    trade_type = models.CharField(max_length=16, blank=True, null=True)  # 交易类型
    bank_type = models.CharField(max_length=16, blank=True, null=True)
    total_fee = models.PositiveIntegerField(blank=True, null=True)  # 订单总金额，单位为分
    fee_type = models.CharField(max_length=8, blank=True, null=True)  # 货币种类
    cash_fee = models.PositiveIntegerField(blank=True, null=True)  # 现金支付金额
    cash_fee_type = models.CharField(max_length=16, blank=True, null=True)  # 现金支付货币类型
    coupon_fee = models.PositiveIntegerField(blank=True, null=True)  # 代金券或立减优惠金额
    coupon_count = models.PositiveIntegerField(blank=True, null=True)  # 代金券或立减优惠使用数量
    out_trade_no = models.CharField(max_length=32, blank=True, null=True)  # 商户系统的订单号，与请求一致
    attach = models.CharField(max_length=128, blank=True, null=True)  # 商家数据包，原样返回
    # 支付完成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010
    time_end = models.CharField(max_length=16, blank=True, null=True)

    # 查询订单解口 orderquery返回
    trade_state = models.CharField(max_length=32, blank=True, null=True, choices=PaymentStatus.CHOICES)  # 交易状态
    # 交易状态描述,对当前查询订单状态的描述和下一步操作的指引
    trade_state_desc = models.CharField(max_length=256, blank=True, null=True)
    xml_response = models.TextField(blank=True, null=True)  # 原始xml信息

    def parse_xml_resp(self, xml_resp):
        pass



