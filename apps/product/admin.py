from django.contrib import admin
from models import Brand, Product
from utils.custom_admin_site import member_site

admin.site.register(Brand)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_pic_link', 'name_en', 'avg_sell_price')
    ordering = ['brand']
    search_fields = ('name_en', 'name_cn', 'brand__name_en', 'brand__name_cn')


admin.site.register(Product, ProductAdmin)
member_site.register(Product, ProductAdmin)
