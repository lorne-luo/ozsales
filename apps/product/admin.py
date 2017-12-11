from django.contrib import admin
from models import Category, Brand, Product
from utils.custom_admin_site import member_site

admin.site.register(Category)


class BrandAdmin(admin.ModelAdmin):
    # ordering = ['category']
    pass


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_pic_link', 'name_en', 'safe_sell_price', 'normal_price', 'bargain_price')
    ordering = ['brand']
    search_fields = ('name_en', 'name_cn', 'brand__name_en', 'brand__name_cn')


admin.site.register(Product, ProductAdmin)
member_site.register(Product, ProductAdmin)
