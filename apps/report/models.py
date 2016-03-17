import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from apps.order.models import Order, ORDER_STATUS

# Create your models here.
@python_2_unicode_compatible
class MonthlyReport(models.Model):
    month = models.DateField(auto_now_add=False, editable=True, blank=False, null=False,
                             verbose_name=_(u'Month'))
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

    @staticmethod
    def stat(stat_date):
        if not isinstance(stat_date, datetime.date) and not isinstance(stat_date, datetime.datetime):
            raise

        stat_date = stat_date.replace(day=1)
        report_filter = MonthlyReport.objects.filter(month=stat_date)
        if report_filter.count():
            report = report_filter[0]
        else:
            report = MonthlyReport()
            report.month = stat_date

        report.reset()

        all_orders = Order.objects.all()
        for order in all_orders:
            if order.is_paid and order.paid_time:
                if order.paid_time.year == stat_date.year and order.paid_time.month == stat_date.month:
                    report.cost_aud += order.total_cost_aud
                    report.cost_rmb += order.total_cost_rmb
                    report.shipping_fee += order.shipping_fee
                    report.sell_price_rmb += order.sell_price_rmb
                    report.profit_rmb += order.profit_rmb
        report.save()
