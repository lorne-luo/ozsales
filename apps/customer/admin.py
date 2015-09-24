from django.forms import ModelForm
from django.contrib import admin
from models import Customer, Address, InterestTag
from forms import CustomerAddForm, AddressAddInline, AddressChangeInline, InterestTagInline
from ..order.forms import OrderInline


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_order_link', 'mobile', 'order_count', 'last_order_time')
    search_fields = ('name', 'mobile')
    inlines = [AddressAddInline, ]
    ordering = ['-last_order_time']

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['password', 'groups', 'user_permissions', 'last_login', 'primary_address']
        self.form = ModelForm
        self.inlines = [AddressAddInline]

        return super(CustomerAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ['password', 'groups', 'user_permissions', 'last_login']
        self.form = CustomerAddForm
        self.inlines = [AddressChangeInline, OrderInline]
        return super(CustomerAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.save()


admin.site.register(Customer, CustomerAdmin)


class AddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'address', 'get_customer_link', 'id_photo_link')


admin.site.register(Address, AddressAdmin)

admin.site.register(InterestTag)

