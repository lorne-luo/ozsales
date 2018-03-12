# coding=utf-8
import datetime
from django.db import models
from dateutil.relativedelta import relativedelta
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import F, Sum, Count
from django.utils import timezone

from apps.customer.models import Customer, Address
from apps.express.models import ExpressOrder
from apps.member.models import Seller
from apps.order.models import Order, ORDER_STATUS


# Create your models here.
@python_2_unicode_compatible
class MonthlyReport(models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    month = models.DateField(auto_now_add=False, editable=True, blank=False, null=False,
                             verbose_name=_(u'Month'))
    order_count = models.PositiveIntegerField(blank=True, null=True)
    parcel_count = models.PositiveIntegerField(blank=True, null=True)
    cost_aud = models.DecimalField(_(u'Cost AUD'), max_digits=8, decimal_places=2, default=0)
    cost_rmb = models.DecimalField(_(u'Cost RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    shipping_fee = models.DecimalField(_(u'Shipping Fee'), max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price_rmb = models.DecimalField(_(u'Sell Price RMB'), max_digits=8, decimal_places=2, blank=True, null=True)
    profit_rmb = models.DecimalField(_(u'Profit RMB'), max_digits=8, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '[%s]%s' % (self.month.strftime('%Y-%b'), self.profit_rmb)

    def reset(self):
        self.cost_aud = 0
        self.cost_rmb = 0
        self.shipping_fee = 0
        self.sell_price_rmb = 0
        self.profit_rmb = 0
        self.order_count = 0
        self.parcel_count = 0

    @staticmethod
    def stat_current_month(user):
        seller = user.profile
        if isinstance(seller, Seller):
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            MonthlyReport.stat_month(seller, year, month)

    @staticmethod
    def stat_month(user, year, month):
        seller = user.profile
        if not isinstance(seller, Seller):
            return
        stat_date = datetime.date(year=year, month=month, day=1)
        next_month_future = timezone.now() + relativedelta(months=1)
        next_month_future = datetime.date(year=next_month_future.year, month=next_month_future.month, day=1)
        if stat_date > next_month_future:
            # input month still not coming
            return

        report = MonthlyReport.objects.filter(seller=seller, month=stat_date).first()
        if not report:
            report = MonthlyReport(seller=seller)
            report.month = stat_date

        report.reset()

        all_orders = Order.objects.filter(seller=seller, is_paid=True, create_time__year=year,
                                          create_time__month=month).exclude(status=ORDER_STATUS.CREATED).annotate(
            express_orders_count=Count('express_orders'))

        if all_orders.count():
            sum_object = all_orders.aggregate(total_cost_aud=Sum(F('total_cost_aud')),
                                              total_cost_rmb=Sum(F('total_cost_rmb')),
                                              shipping_fee=Sum(F('shipping_fee')),
                                              sell_price_rmb=Sum(F('sell_price_rmb')),
                                              parcel_count=Sum(F('express_orders_count')),
                                              profit_rmb=Sum(F('profit_rmb')))

            report.order_count = all_orders.count()
            report.cost_aud = sum_object.get('total_cost_aud', 0)
            report.cost_rmb = sum_object.get('total_cost_rmb', 0)
            report.shipping_fee = sum_object.get('shipping_fee', 0)
            report.sell_price_rmb = sum_object.get('sell_price_rmb', 0)
            report.profit_rmb = sum_object.get('profit_rmb', 0)
            report.parcel_count = sum_object.get('parcel_count', 0)
            report.save()

    @staticmethod
    def stat_user_total(user):
        if not user.is_seller:
            return Http404
        seller = user.profile

        if not Order.objects.filter(seller=seller).count():
            return {}

        first_day = Order.objects.filter(seller=seller).order_by('create_time').first().create_time
        distance = timezone.now() - first_day

        own_orders = Order.objects.filter(seller=seller)
        data = own_orders.aggregate(total_amount=Sum('total_amount'), total_sell_price=Sum('sell_price_rmb'),
                                    total_cost_aud=Sum('product_cost_aud'), total_profit_rmb=Sum('profit_rmb'),
                                    total_express_fee=Sum('shipping_fee'))

        data.update({'first_day': first_day,
                     'total_year': distance.days / 365,
                     'total_day': distance.days % 365,
                     'total_customer': Customer.objects.filter(seller=seller).count(),
                     'total_order': own_orders.count(),
                     'total_address': Address.objects.filter(customer__seller=seller).count(),
                     'total_expressorder': ExpressOrder.objects.filter(order__seller=seller).count(),
                     })
        data.update(own_orders.filter(is_paid=False).aggregate(total_unpaid_amount=Sum('sell_price_rmb')))
        return data
