from django.contrib import admin
from models import ExpressOrder, ExpressCompany


admin.site.register(ExpressCompany)

class ExpressOrderAdmin(admin.ModelAdmin):
    list_display = ('carrier', 'id_number', 'order', 'shipping_fee', 'weight','remarks')

admin.site.register(ExpressOrder,ExpressOrderAdmin)
