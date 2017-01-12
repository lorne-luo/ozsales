from django.contrib import admin
from models import Seller

# Register your models here.

class SellerAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'mobile', 'is_staff', 'is_active', 'date_joined')

admin.site.register(Seller, SellerAdmin)
