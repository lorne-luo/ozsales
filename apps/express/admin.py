from django.contrib import admin
from models import ExpressOrder, ExpressCarrier

admin.site.register(ExpressCarrier)


class ExpressOrderAdmin(admin.ModelAdmin):
    list_display = ('carrier', 'get_tracking_link', 'get_order_link', 'address', 'fee', 'weight', 'create_time')
    ordering = ['-create_time']
    list_display_links = ['address', 'carrier']
    search_fields = ('order__customer__name', 'address__name', 'track_id', 'carrier_name_cn', 'carrier_name_en')


admin.site.register(ExpressOrder, ExpressOrderAdmin)
