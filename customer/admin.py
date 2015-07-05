from django.contrib import admin
from customer.models import Customer, Address, InterestTag
# Register your models here.

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'Address'


class InterestTagInline(admin.TabularInline):
    model = InterestTag
    extra = 1
    can_delete = True
    # max_num = 1
    verbose_name_plural = 'Tag'


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile')
    search_fields = ('name', 'mobile')

    def add_view(self, request, form_url='', extra_context=None):
        self.exclude = ['password', 'groups', 'user_permissions', 'last_login']
        self.inlines = [AddressInline, ]
        return super(CustomerAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.exclude = ['password', 'groups', 'user_permissions']
        self.inlines = [AddressInline, ]
        return super(CustomerAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Customer, CustomerAdmin)

admin.site.register(Address)

admin.site.register(InterestTag)

