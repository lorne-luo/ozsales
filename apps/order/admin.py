from django.contrib import admin
from django.forms import ModelForm

from models import Order, OrderProduct
from form import OrderAddForm
from ..express.form import ExpressOrderAddInline, ExpressOrderChangeInline


class OrderProductAddInline(admin.TabularInline):
    exclude = ['total_price_aud', 'total_price_rmb']
    model = OrderProduct
    extra = 2
    # max_num = 1
    verbose_name_plural = 'OrderProduct'


class OrderProductChangeInline(admin.TabularInline):
    model = OrderProduct
    extra = 1
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'OrderProduct'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'status_button', 'product_cost_aud', 'shipping_fee', 'total_cost_aud',
                    'sell_price', 'profit_rmb', 'create_time')
    list_filter = ['status']
    inlines = []

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [OrderProductAddInline, ExpressOrderAddInline]
        self.exclude = ['total_amount', 'total_product_price_aud', 'total_product_price_rmb', 'shipping_fee', 'status',
                        'total_price_aud', 'total_price_rmb', 'profit_rmb']
        self.form = OrderAddForm
        return super(OrderAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [OrderProductChangeInline, ExpressOrderChangeInline]
        self.exclude = []
        self.form = ModelForm
        return super(OrderAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)


