# coding=utf-8
from django.core.urlresolvers import reverse
from rest_framework import serializers
from .models import Customer, Address


# class CustomerSerializer(serializers.ModelSerializer):
#     primary_address = serializers.CharField()
#     name = serializers.SerializerMethodField('get_link')
#
#     class Meta:
#         model = Customer
#         fields = Customer.Config.list_display_fields + ('id',)
#         read_only_fields = (
#             'id', 'date_joined'
#         )
#
#     def get_link(self, obj):
#         request = self.context.get('request', None)
#         change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
#         view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
#         if request.user.has_perm(change_perm_str):
#             return obj.get_edit_link()
#         elif request.user.has_perm(view_perm_str):
#             return obj.get_detail_link()
#         return obj.name


# Serializer for address
class AddressSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    customer_link = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['link', 'name', 'mobile', 'address', 'customer', 'id_number', 'id_photo_front', 'customer_link',
                  'id_photo_back', 'id']
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            url = reverse('customer:address-update', args=[obj.id])
            return u'<a href="%s">%s</a>' % (url, obj.name)
        elif request.user.has_perm(view_perm_str):
            url = reverse('customer:address-detail', args=[obj.id])
            return u'<a href="%s">%s</a>' % (url, obj.name)
        return None

    def get_customer_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            return obj.customer.get_edit_link()
        elif request.user.has_perm(view_perm_str):
            return obj.customer.get_detail_link()
        return None


# Serializer for customer
class CustomerSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    primary_address_display = serializers.CharField(source='primary_address')

    class Meta:
        model = Customer
        fields = ['link'] + ['last_login', 'seller', 'name', 'email', 'mobile', 'order_count',
                             'primary_address', 'primary_address_display', 'tags', 'id']
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            url = reverse('customer:customer-update', args=[obj.id])
            return u'<a href="%s">%s</a>' % (url, obj.name)
        elif request.user.has_perm(view_perm_str):
            url = reverse('customer:customer-detail', args=[obj.id])
            return u'<a href="%s">%s</a>' % (url, obj.name)
        return None
