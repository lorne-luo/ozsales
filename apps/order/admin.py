from django.contrib import admin
from django.forms import ModelForm

from models import Order, OrderProduct
from forms import OrderForm
from ..express.forms import ExpressOrderAddInline, ExpressOrderChangeInline


class OrderProductAddInline(admin.TabularInline):
    exclude = ['total_price_aud', 'total_price_rmb']
    model = OrderProduct
    extra = 1
    # max_num = 1
    can_delete = True
    verbose_name_plural = 'Order Products'


class OrderProductChangeInline(admin.TabularInline):
    model = OrderProduct
    extra = 1
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'Order Products'


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_time', 'get_customer_link', 'total_amount', 'get_status_button',
                    'sell_price_rmb', 'get_id_upload', 'get_paid_button', 'profit_rmb', 'product_cost_aud',
                    'shipping_fee',
                    'origin_sell_rmb', 'total_cost_aud', 'total_cost_rmb', 'sell_price_rmb')
    list_filter = ['status']
    ordering = ['-create_time']
    inlines = []
    readonly_fields = ['total_amount', 'product_cost_aud', 'product_cost_rmb', 'shipping_fee',
                       'total_cost_aud', 'total_cost_rmb', 'origin_sell_rmb', 'profit_rmb', 'create_time']
    exclude = ['ship_time', ]
    list_display_links = ['id', 'total_amount', 'product_cost_aud', 'shipping_fee', 'origin_sell_rmb', 'total_cost_aud',
                          'total_cost_rmb', 'sell_price_rmb', 'profit_rmb']
    search_fields = ('customer__name',)

    def add_view(self, request, form_url='', extra_context=None):
        self.inlines = [OrderProductAddInline, ExpressOrderAddInline]
        self.exclude = ['total_amount', 'total_product_price_aud', 'total_product_price_rmb', 'shipping_fee', 'status',
                        'total_price_aud', 'total_price_rmb', 'profit_rmb']
        self.form = OrderForm
        return super(OrderAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = [OrderProductChangeInline, ExpressOrderChangeInline]
        self.exclude = []
        self.form = OrderForm
        return super(OrderAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Order, OrderAdmin)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'order', 'amount', 'sell_price_rmb', 'cost_price_aud', 'store', 'create_time')
    search_fields = ('name', 'product__name_en', 'product__name_cn')


admin.site.register(OrderProduct, OrderProductAdmin)


