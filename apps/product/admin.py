from django.contrib import admin
from models import Category, Brand, Product

admin.site.register(Category)


class BrandAdmin(admin.ModelAdmin):
    # ordering = ['category']
    pass


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_pic_link', 'get_name_cn', 'safe_sell_price', 'normal_price', 'bargain_price')
    ordering = ['brand']
    search_fields = ('name_en', 'name_cn', 'brand__name_en', 'brand__name_cn')


admin.site.register(Product, ProductAdmin)
