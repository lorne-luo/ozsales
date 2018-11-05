# coding=utf-8
import logging
from decimal import Decimal
from enum import Enum

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from django.utils.crypto import get_random_string
from apps.member.models import Seller
from core.django.constants import CURRENCY_CHOICES
from core.aliyun.sms.service import send_cn_sms
from core.django.models import TenantModelMixin
from ..schedule.models import forex
from weixin.pay import WeixinPay, WeixinError, WeixinPayError
from ..product.models import Product
from ..customer.models import Customer, Address
from ..store.models import Store

log = logging.getLogger(__name__)


class ORDER_STATUS(object):
    CREATED = 'CREATED'
    CONFIRMED = 'CONFIRMED'
    SHIPPING = 'SHIPPING'
    DELIVERED = 'DELIVERED'
    FINISHED = 'FINISHED'
    CANCELED = 'CANCELED'
    CLOSED = 'CLOSED'


ORDER_STATUS_CHOICES = (
    (ORDER_STATUS.CREATED, '创建'),
    # (ORDER_STATUS.CONFIRMED, u'确认'),
    (ORDER_STATUS.SHIPPING, '在途'),
    (ORDER_STATUS.DELIVERED, '寄达'),
    (ORDER_STATUS.FINISHED, '完成'),
    # (ORDER_STATUS.CANCELED, u'取消'),
    (ORDER_STATUS.CLOSED, '关闭')
)


class OrderManager(models.Manager):
    def new(self):
        qs = super(OrderManager, self).get_queryset()
        return qs.filter(Q(status=ORDER_STATUS.CREATED) | Q(is_paid=False))

    def shipping(self):
        qs = super(OrderManager, self).get_queryset()
        return qs.filter(Q(status=ORDER_STATUS.SHIPPING) | Q(status=ORDER_STATUS.DELIVERED), is_paid=True)

    def finished(self):
        return super(OrderManager, self).get_queryset().filter(status=ORDER_STATUS.FINISHED)


class Order(TenantModelMixin, models.Model):
    uid = models.CharField(unique=True, max_length=12, null=True, blank=True)
    seller = models.ForeignKey(Seller, blank=True, null=True)
    customer = models.ForeignKey(Customer, blank=False, null=False, verbose_name=_('客户'))
    address = models.ForeignKey(Address, blank=True, null=True, verbose_name=_('地址'))
    address_text = models.CharField(_('地址'), max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name=_('已支付'))
    paid_time = models.DateTimeField(auto_now_add=False, editable=True, blank=True, null=True, verbose_name=_('支付时间'))
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=ORDER_STATUS.CREATED,
                              verbose_name=_('状态'))
    total_amount = models.IntegerField(_('数量'), default=0, blank=False, null=False)
    product_cost_aud = models.DecimalField(_('货物成本'), max_digits=8, decimal_places=2, blank=True, null=True)
    product_cost_rmb = models.DecimalField(_('货物成本'), max_digits=8, decimal_places=2, blank=True, null=True)
    shipping_fee = models.DecimalField(_('快递费用'), max_digits=8, decimal_places=2, blank=True, null=True)
    ship_time = models.DateTimeField(auto_now_add=False, editable=True, blank=True, null=True, verbose_name=_('寄出时间'))
    currency = models.CharField(_('货币'), max_length=128, choices=CURRENCY_CHOICES, blank=True)
    total_cost_aud = models.DecimalField(_('总成本'), max_digits=8, decimal_places=2, blank=True, null=True)
    total_cost_rmb = models.DecimalField(_('总承包'), max_digits=8, decimal_places=2, blank=True, null=True)
    origin_sell_rmb = models.DecimalField(_('原价'), max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price_rmb = models.DecimalField(_('售价'), max_digits=8, decimal_places=2, blank=True, null=True)
    payment_price = models.DecimalField(_('Payment Price'), max_digits=8, decimal_places=2, blank=True, null=True)
    remark = models.CharField(max_length=512, blank=True, null=True, verbose_name=_('remark'))
    profit_rmb = models.DecimalField(_('利润'), max_digits=8, decimal_places=2, blank=True, null=True)
    aud_rmb_rate = models.DecimalField(_('下单汇率'), max_digits=8, decimal_places=4, blank=True, null=True)
    create_time = models.DateTimeField(_('创建时间'), auto_now_add=True, editable=False)
    finish_time = models.DateTimeField(_('完成时间'), editable=True, blank=True, null=True)
    coupon = models.CharField(_('Coupon'), max_length=30, null=True, blank=True)
    app_id = models.CharField(_('App ID'), max_length=128, null=True, blank=True)

    shipping_msg_sent = models.BooleanField(_(u'send msg'), default=False, null=False, blank=False)  # 寄出通知
    delivery_msg_sent = models.BooleanField(_(u'delivery msg'), default=False, null=False, blank=False)  # 寄达通知

    objects = OrderManager()

    class Meta:
        get_latest_by = "finish_time"

    def __str__(self):
        if not self._state.adding:
            return '[%s]%s' % (self.uid, self.customer.name)
        else:
            return '%s' % (self.customer.name)

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self._currency_original = self.currency

    @classmethod
    def generate_uid(cls):
        # 3 alphabet and 3 number
        alphabets = get_random_string(2, 'abcdefghijklmnopqrstuvwxyz')
        mid = get_random_string(1, 'abcdefghijklmnopqrstuvwxyz1234567890')
        numbers = get_random_string(3, '1234567890')
        return alphabets + mid + numbers

    def set_uid(self):
        if not self.uid:
            uid = self.generate_uid()
            while Order.objects.filter(uid=uid).exists():
                uid = self.generate_uid()
            self.uid = uid

    def get_customer_mobile(self):
        if self.customer and self.customer.mobile:
            return self.customer.mobile
        return None

    def sms_shipping(self):
        if not self.seller.is_premium:
            return

        mobile = self.get_customer_mobile()
        if not mobile or self.shipping_msg_sent:
            return

        bz_id = 'Order#%s-sent' % self.pk
        data = '''{"url":"%s", "count":"%s"}''' % (self.public_url, self.express_orders.count())
        template = settings.ORDER_SENT_PAID_TEMPLATE if self.is_paid else settings.ORDER_SENT_UNPAID_TEMPLATE
        success, detail = send_cn_sms(bz_id, mobile, template, data)
        if success:
            self.shipping_msg_sent = True
            self.save(update_fields=['shipping_msg_sent'])

    def sms_delivered(self):
        if not self.seller.is_premium:
            return

        mobile = self.get_customer_mobile()
        if not mobile or self.delivery_msg_sent:
            return

        # all delivered, send ORDER_DELIVERED_TEMPLATE
        if self.is_all_delivered:
            bz_id = 'Order#%s-delivered' % self.pk
            data = '''{"url":"%s"}''' % self.public_url
            success, detail = send_cn_sms(bz_id, mobile, settings.ORDER_DELIVERED_TEMPLATE, data)
            if success:
                self.delivery_msg_sent = True
                self.save(update_fields=['delivery_msg_sent'])
                self.express_orders.all().update(delivery_sms_sent=True)
            return

        # part of parcels delivered, send PACKAGE_DELIVERED_TEMPLATE
        need_sms = self.express_orders.filter(is_delivered=True, delivery_sms_sent=False)
        track_ids = [x.track_id for x in need_sms]
        if track_ids:
            bz_id = 'OrderParcels#%s-delivered' % self.pk
            track_id = ','.join(track_ids)
            data = '''{"track_id":"%s", "url":"%s"}''' % (track_id, self.public_url)
            success, detail = send_cn_sms(bz_id, mobile, settings.PACKAGE_DELIVERED_TEMPLATE, data)
            if success:
                need_sms.update(delivery_sms_sent=True)

    def get_product_summary(self):
        result = ''
        for product in self.products.all():
            result += '%s <br/>' % product.get_summary()
        return result

    def get_summary(self):
        """ plain text summary for order """
        if self.customer:
            url = reverse('admin:%s_%s_change' % ('customer', 'customer'), args=[self.customer.pk])
            result = '<br/><a href="%s">%s</a>' % (url, str(self.address))
        else:
            result = 'None'

        if self.address:
            if self.address.id_number:
                result += '<br/><br/>  <span>%s %s</span>' % (self.address.name, self.address.id_number)
        result += '<br/><br/>'

        if self.products.count():
            result += self.get_product_summary()
            result += '总计: %d<br/>' % self.sell_price_rmb
            result = '%s<br/><br/><br/>' % result
        return result

    def set_paid(self):
        self.is_paid = True
        self.paid_time = timezone.now()
        self.set_finish_time()
        self.save()
        self.update_monthly_report()

    def set_finish_time(self):
        if self.is_paid and not self.finish_time and self.status in [ORDER_STATUS.SHIPPING,
                                                                     ORDER_STATUS.DELIVERED,
                                                                     ORDER_STATUS.FINISHED]:
            self.finish_time = timezone.now()

    def set_status(self, status_value):
        self.status = status_value
        if status_value == ORDER_STATUS.FINISHED:
            if self.is_paid:
                self.products.update(is_purchased=True)
                self.express_orders.update(is_delivered=True)
                customer = self.customer
                customer.last_order_time = self.create_time
                customer.order_count = customer.order_set.filter(status__in=[ORDER_STATUS.SHIPPING,
                                                                             ORDER_STATUS.DELIVERED,
                                                                             ORDER_STATUS.FINISHED]).count()
                customer.save(update_fields=['last_order_time', 'order_count'])
            else:
                return

            self.set_finish_time()
        self.save()
        if status_value == ORDER_STATUS.SHIPPING:
            self.sms_shipping()
        self.update_price()

    def update_monthly_report(self):
        if self.is_paid and not self.status == ORDER_STATUS.CREATED:
            if not self.paid_time:
                self.paid_time = timezone.now()
                self.save(update_fields=['paid_time'])

            from ..report.models import MonthlyReport
            MonthlyReport.stat_month(self.create_time.year, self.create_time.month)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.set_uid()
        if not self.address and self.customer and self.customer.primary_address:
            self.address = self.customer.primary_address

        if self.address:
            self.address_text = self.address.get_text()

        if self._state.adding or self._currency_original != self.currency:
            # new creating or currency changed, update forex rate
            self.aud_rmb_rate = getattr(forex, self.currency or self.seller.primary_currency)

        self.total_cost_aud = self.product_cost_aud or 0
        self.product_cost_rmb = self.total_cost_aud * self.get_aud_rmb_rate()

        self.total_cost_aud += self.shipping_fee or 0
        self.total_cost_rmb = self.total_cost_aud * self.get_aud_rmb_rate()

        if self.sell_price_rmb is not None and self.total_cost_rmb is not None:
            self.profit_rmb = self.sell_price_rmb - self.total_cost_rmb

        super(Order, self).save(force_insert, force_update, using, update_fields)

    def get_total_fee(self):
        # 微信支付金额单位:分
        return int(self.payment_price * 100)

    def get_link(self):
        url = reverse('admin:%s_%s_change' % ('order', 'order'), args=[self.pk])
        name = '[#%s]%s' % (self.pk, self.customer.name)
        return '<a href="%s">%s</a>' % (url, name)

    @property
    def public_url(self):
        return reverse('order-detail-short', args=[self.schema_id, self.uid])

    def get_aud_rmb_rate(self):
        if self.aud_rmb_rate:
            return self.aud_rmb_rate

        return getattr(forex, self.currency or self.seller.primary_currency)

    def update_price(self, update_sell_price=False):
        if not self.products.count() and not self.express_orders.count():
            return

        self.total_amount = 0
        self.product_cost_aud = 0
        self.product_cost_rmb = 0
        self.origin_sell_rmb = 0
        self.shipping_fee = 0
        self.profit_rmb = 0

        products = self.products.all()
        for p in products:
            self.total_amount += p.amount
            self.product_cost_aud += p.amount * p.cost_price_aud
            self.origin_sell_rmb += p.sell_price_rmb * p.amount
            if p.product:
                p.product.stat()

        express_orders = self.express_orders.all()
        for ex_order in express_orders:
            self.ship_time = ex_order.create_time
            if ex_order.fee:
                self.shipping_fee += ex_order.fee

        if self.origin_sell_rmb % 1 < Decimal(0.02):
            self.origin_sell_rmb = Decimal(int(self.origin_sell_rmb)).quantize(Decimal('.01'))

        if self.sell_price_rmb is None and self.products.count() or update_sell_price:
            # init assignment or force update from product.post_save and expressorder.post_save
            self.sell_price_rmb = self.origin_sell_rmb
        elif self.products.count() == 0:
            self.sell_price_rmb = 0
            self.total_amount = 0

        post_save.disconnect(update_price_from_order, sender=Order)
        self.save()
        self.update_monthly_report()
        post_save.connect(update_price_from_order, sender=Order)

    def get_paid_button(self):
        if not self.is_paid:
            url = reverse('order:change-order-paid', kwargs={'order_id': self.pk})
            return '<a href="%s"><b>UNPAID</b></a>' % url
        return 'PAID'

    get_paid_button.allow_tags = True
    get_paid_button.short_description = 'Paid'

    def get_status_button(self):
        current_status = self.get_shipping_orders()
        if self.status in [ORDER_STATUS.CREATED, ORDER_STATUS.DELIVERED]:
            current_status += '<b>%s</b>' % self.status
        else:
            current_status += self.status

        next_status = self.next_status

        if not next_status:
            return ORDER_STATUS.FINISHED

        url = self.get_next_status_url()
        btn = '%s => <a href="%s">%s</a>' % (current_status, url, next_status)
        return btn

    def get_next_status_url(self):
        url = reverse('order:change-order-status', kwargs={'order_id': self.pk, 'status_value': self.next_status})
        return url

    @property
    def next_status(self):
        if self.status == ORDER_STATUS.CREATED:
            return ORDER_STATUS.SHIPPING
        elif self.status == ORDER_STATUS.SHIPPING:
            return ORDER_STATUS.DELIVERED
        elif self.status == ORDER_STATUS.DELIVERED:
            return ORDER_STATUS.FINISHED
        else:
            return None

    def get_shipping_orders(self):
        result = ''
        for ex in self.express_orders.all():
            if self.status not in [ORDER_STATUS.FINISHED, ORDER_STATUS.CANCELED,
                                   ORDER_STATUS.CLOSED] and ex.is_delivered:
                result += '<u>%s</u><br/>' % ex.get_tracking_link()
            else:
                result += ex.get_tracking_link() + '<br/>'
        return result

    get_status_button.allow_tags = True
    get_status_button.short_description = 'Shipping Status'

    def get_id_upload(self):
        express_orders = self.express_orders.all()

        for ex_order in express_orders:
            if not ex_order.id_upload:
                return '<a target="_blank" href="%s"><b>UPLOAD</b></a>' % ex_order.carrier.website
        if not express_orders.count():
            return 'No Shipping'
        return 'DONE'

    get_id_upload.short_description = 'ID Upload'
    get_id_upload.allow_tags = True

    def get_customer_link(self):
        return self.customer.get_link()

    get_customer_link.allow_tags = True
    get_customer_link.short_description = 'Customer'

    def notify_delivered(self):
        subject = '%s 全部寄达.' % self
        content = '<a target="_blank" href="%s">%s</a> 全部寄达.' % (self.public_url, self)

        self.seller.send_notification(subject, content)
        # self.seller.send_email(subject, content)
        # self.customer.send_email(subject, content)

    def get_track_express(self):
        """get express order need to be track"""
        skip_days = 2  # skip recent creation
        two_days_ago = timezone.now() - relativedelta(days=skip_days)
        return self.express_orders.filter(create_time__lt=two_days_ago,
                                          is_delivered=False,
                                          carrier__isnull=False)

    def update_track(self):
        express_all = self.get_track_express()
        if express_all.count() == 0:
            return

        all_delivered = True
        for express in express_all:
            express.update_track()
            if not express.is_delivered:
                all_delivered = False

        if all_delivered:
            self.set_status(ORDER_STATUS.DELIVERED)
            # notify seller and customer
            self.sms_delivered()
            self.notify_delivered()

    @cached_property
    def is_all_delivered(self):
        parcels = self.express_orders.all()
        return parcels.count() and parcels.filter(is_delivered=False).count() == 0

    @property
    def app(self):
        from ..weixin.models import WxApp
        app = WxApp.objects.get(app_id=self.app_id)
        return app

    def get_wxorder(self, user_ip, trade_type="JSAPI"):
        from ..weixin.models import WxOrder

        wx_order = self.wxorder if self.wxorder else WxOrder(order=self)
        if wx_order.is_success:
            if self.get_total_fee() == wx_order.total_fee:
                return wx_order
            else:
                # order price changed, delete old create new
                wx_order.delete()
                wx_order = WxOrder(order=self)

        # request weixin unified order api
        try:
            raw = self.app.pay.unified_order(trade_type=trade_type, openid=self.openid, body=self.uuid,
                                             out_trade_no=self.uuid,
                                             total_fee=self.get_total_fee(), spbill_create_ip=user_ip)
        except WeixinError as e:
            log.info(e.message)
            return None

        wx_order.return_code = raw.return_code
        wx_order.return_msg = raw.return_msg
        wx_order.result_code = raw.result_code
        wx_order.appid = raw.app_id
        wx_order.mch_id = raw.mch_id
        wx_order.device_info = raw.device_info
        wx_order.nonce_str = raw.nonce_str
        wx_order.sign = raw.sign
        wx_order.err_code = raw.err_code
        wx_order.err_code_des = raw.err_code_des
        wx_order.trade_type = raw.trade_type
        wx_order.prepay_id = raw.prepay_id
        wx_order.total_fee = self.get_total_fee()

        wx_order.save()
        return wx_order

    def get_jsapi(self, ip):
        # create wx order and get jsapi
        wx_order = self.get_wxorder(ip)
        return wx_order.get_jsapi()


class OrderProduct(TenantModelMixin, models.Model):
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_('Order'), related_name='products')
    product = models.ForeignKey(Product, blank=True, null=True, verbose_name=_('Product'))
    name = models.CharField(_('Name'), max_length=128, null=True, blank=True, help_text='产品名称')
    description = models.CharField(_('Description'), max_length=128, null=True, blank=True, help_text='备注')
    amount = models.IntegerField(_('Amount'), default=1, blank=False, null=False, help_text='数量')
    sell_price_rmb = models.DecimalField(_('Sell Price RMB'), max_digits=8, decimal_places=2, default=0, blank=False,
                                         null=False, help_text='单价')
    total_price_rmb = models.DecimalField(_('Total RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    cost_price_aud = models.DecimalField(_('Cost Price AUD'), max_digits=8, decimal_places=2, default=0, blank=False,
                                         null=False, help_text='成本')
    total_price_aud = models.DecimalField(_('Total AUD'), max_digits=8, decimal_places=2, blank=True, null=True)
    store = models.ForeignKey(Store, blank=True, null=True, verbose_name=_('Store'))
    is_purchased = models.BooleanField(default=False)
    create_time = models.DateTimeField(_('Create Time'), auto_now_add=True, editable=True)

    class Meta:
        ordering = ['create_time']

    def __str__(self):
        return '%s = %d X %s' % (self.name, self.sell_price_rmb, self.amount)

    def get_last_sale(self):
        last_sale = OrderProduct.objects.filter(order__seller_id=self.order.seller_id, product_id=self.product_id
                                                ).exclude(sell_price_rmb=0
                                                          ).exclude(pk=self.pk).order_by('-create_time').first()
        return last_sale

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.amount is None:
            self.amount = 1

        if self.cost_price_aud is None or self.sell_price_rmb is None:
            last_sale = self.get_last_sale()
            if last_sale:
                self.cost_price_aud = self.cost_price_aud if self.cost_price_aud else last_sale.cost_price_aud
                self.sell_price_rmb = self.sell_price_rmb if self.sell_price_rmb else last_sale.sell_price_rmb
            else:
                self.cost_price_aud = self.cost_price_aud if self.cost_price_aud else 0
                self.sell_price_rmb = self.sell_price_rmb if self.sell_price_rmb else 0

        self.total_price_aud = self.cost_price_aud * self.amount
        self.total_price_rmb = self.sell_price_rmb * self.amount

        if self.product:
            self.name = str(self.product)

        if self.description:
            self.name += ' %s' % self.description

        return super(OrderProduct, self).save(force_insert, force_update, using, update_fields)

    def get_summary(self):
        description = ' %s' % self.description if self.description else ''
        return '%s%s = ¥%d x %d' % (self.name, description, self.sell_price_rmb, self.amount)

    def get_link(self):
        if self.product:
            return reverse('product:product-detail', args=[self.product.pk])
        else:
            return None


@receiver(post_save, sender=Order)
def update_price_from_order(sender, instance=None, created=False, update_fields=None, **kwargs):
    if update_fields:
        if 'status' in update_fields or 'is_paid' in update_fields or 'paid_time' in update_fields:
            instance.update_monthly_report()
    elif instance.pk:
        if instance.products.count() or instance.express_orders.count():
            instance.update_price()


@receiver(post_save, sender=OrderProduct)
def update_price_from_orderproduct(sender, instance=None, created=False, update_fields=None, **kwargs):
    if instance.order and instance.order.pk:
        instance.order.update_price(update_sell_price=True)


@receiver(post_delete, sender=OrderProduct)
def order_product_deleted(sender, **kwargs):
    instance = kwargs['instance']
    instance.order.update_price(update_sell_price=True)


def confirm_order_from_cart(cart):
    order = Order(customer=cart.customer, coupon=cart.coupon, payment_price=0, origin_sell_rmb=0)
    order.save()

    for cart_product in cart.products.all():
        product = OrderProduct(product=cart_product.product, order=order, amount=cart_product.amount,
                               name=cart_product.product.get_name_cn(),
                               sell_price_rmb=cart_product.product.safe_sell_price,
                               total_price_rmb=cart_product.amount * cart_product.product.safe_sell_price)
        product.save()
        order.origin_sell_rmb += product.total_price_rmb
        cart_product.delete()

    cart.coupon = None
    cart.save(update_fields=['coupon'])

    # todo coupon
    order.payment_price = order.origin_sell_rmb
    order.save(update_fields=['origin_sell_rmb', 'payment_price'])
