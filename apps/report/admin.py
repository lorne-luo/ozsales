from django.contrib import admin
from .models import MonthlyReport


class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee',
                    'sell_price_rmb', 'profit_rmb')
    list_filter = ['month']
    ordering = ['-month']
    list_display_links = list_display


admin.site.register(MonthlyReport, MonthlyReportAdmin)
