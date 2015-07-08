from django.contrib import admin
from django.forms import ModelForm

from models import Order, OrderProduct
from form import OrderAddForm

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 3
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'OrderProduct'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'total_product_price_rmb', 'shipping_fee', 'total_price_rmb')
    inlines = [OrderProductInline]

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['total_amount', 'total_product_price_aud', 'total_product_price_rmb', 'shipping_fee', 'status', 'total_price_aud', 'total_price_rmb']
        self.form = OrderAddForm

        return super(OrderAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = []
        self.form = ModelForm
        return super(OrderAdmin, self).change_view(request, object_id, form_url, extra_context)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)

