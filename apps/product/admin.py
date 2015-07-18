from django.contrib import admin
from models import Category, Brand, Product

admin.site.register(Category)


class BrandAdmin(admin.ModelAdmin):
    # ordering = ['category']
    pass


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_cn', 'get_pic_link', 'brand', 'normal_price', 'bargain_price', 'safe_sell_price')


admin.site.register(Product, ProductAdmin)
