from django.contrib import admin
from models import ExpressOrder, ExpressCarrier


admin.site.register(ExpressCarrier)


class ExpressOrderAdmin(admin.ModelAdmin):
    list_display = ('carrier', 'get_tracking_link', 'get_order_link', 'shipping_fee', 'weight', 'create_time')


admin.site.register(ExpressOrder, ExpressOrderAdmin)

