from django.contrib import admin
from models import Category, Brand, Product

admin.site.register(Category)

class BrandAdmin(admin.ModelAdmin):
    # ordering = ['category']
    pass

admin.site.register(Brand,BrandAdmin)
admin.site.register(Product)
