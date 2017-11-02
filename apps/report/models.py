# coding=utf-8
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.db.models import F, Sum, Count

from apps.order.models import Order, ORDER_STATUS


# Create your models here.
@python_2_unicode_compatible
class MonthlyReport(models.Model):
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
    def stat_current_month():
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        MonthlyReport.stat(year, month)

    @staticmethod
    def stat(year, month):
        stat_date = datetime.date(year=year, month=month, day=1)
        report_filter = MonthlyReport.objects.filter(month=stat_date)
        if report_filter.count():
            report = report_filter[0]
        else:
            report = MonthlyReport()
            report.month = stat_date

        report.reset()

        all_orders = Order.objects.filter(is_paid=True, create_time__year=year, create_time__month=month).exclude(
            status=ORDER_STATUS.CREATED).annotate(express_orders_count=Count('express_orders'))

        sum_object = all_orders.aggregate(total_cost_aud=Sum(F('total_cost_aud')),
                                          total_cost_rmb=Sum(F('total_cost_rmb')),
                                          shipping_fee=Sum(F('shipping_fee')),
                                          sell_price_rmb=Sum(F('sell_price_rmb')),
                                          parcel_count=Sum(F('express_orders_count')),
                                          profit_rmb=Sum(F('profit_rmb')))

        # for order in all_orders:
        #     if order.customer.name == u'罗韬':
        #         continue
        #     report.cost_aud += order.total_cost_aud
        #     report.cost_rmb += order.total_cost_rmb
        #     report.shipping_fee += order.shipping_fee
        #     report.sell_price_rmb += order.sell_price_rmb
        #     report.profit_rmb += order.profit_rmb
        #     report.parcel_count += order.express_orders.count()

        report.order_count = all_orders.count()
        report.cost_aud = sum_object['total_cost_aud']
        report.cost_rmb = sum_object['total_cost_rmb']
        report.shipping_fee = sum_object['shipping_fee']
        report.sell_price_rmb = sum_object['sell_price_rmb']
        report.profit_rmb = sum_object['profit_rmb']
        report.parcel_count = sum_object['parcel_count']
        report.save()
