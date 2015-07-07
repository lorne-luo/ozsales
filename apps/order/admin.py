from django.contrib import admin
from models import Order, OrderProduct


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
        self.exclude = ['total_amount', 'total_product_price_aud', 'total_product_price_rmb', 'shipping_fee', 'total_price_aud', 'total_price_rmb']

        return super(OrderAdmin, self).add_view(request, form_url, extra_context)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)

