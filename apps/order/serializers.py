# coding=utf-8
from django.core.urlresolvers import reverse
from rest_framework import serializers
from models import OrderProduct, Order, ORDER_STATUS, ORDER_STATUS_CHOICES


# Serializer for order
class OrderSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    address_display = serializers.CharField(source='address')
    customer_display = serializers.CharField(source='customer')
    customer_url = serializers.SerializerMethodField()
    shipping_order = serializers.SerializerMethodField()
    paid_url = serializers.SerializerMethodField()
    public_link = serializers.SerializerMethodField()
    create_time_display = serializers.SerializerMethodField()
    next_status_url = serializers.SerializerMethodField()
    next_status = serializers.SerializerMethodField()
    product_summary = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField()
    sell_price_rmb = serializers.IntegerField()
    shipping_fee = serializers.IntegerField()
    total_cost_aud = serializers.IntegerField()
    total_cost_rmb = serializers.IntegerField()
    profit_rmb = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['link', 'customer', 'customer_display', 'address', 'is_paid', 'status', 'total_amount', 'public_link',
                  'product_cost_aud', 'customer_url', 'shipping_order', 'paid_url', 'next_status_url', 'next_status',
                  'product_summary', 'address_display',
                  'product_cost_rmb', 'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb', 'edit_url',
                  'origin_sell_rmb', 'sell_price_rmb', 'profit_rmb', 'create_time_display', 'finish_time', 'id']
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            url = reverse('order:order-detail-short', args=[obj.customer.id, obj.id])
        elif request.user.has_perm(view_perm_str):
            url = reverse('order:order-detail-short', args=[obj.customer.id, obj.id])
        else:
            url = '#'
        return url

    def get_edit_url(self, obj):
        url = reverse('order:order-update', args=[obj.id])
        return url

    def get_customer_url(self, obj):
        request = self.context.get('request', None)
        if request.user.has_perm('customer.change_customer'):
            return reverse('customer:customer-update', args=[obj.customer.id])
        elif request.user.has_perm('customer.view_customer'):
            return reverse('customer:customer-detail', args=[obj.customer.id])

    def get_shipping_order(self, obj):
        return obj.get_shipping_orders()

    def get_next_status_url(self, obj):
        return obj.get_next_status_url()

    def get_next_status(self, obj):
        return obj.next_status

    def get_paid_url(self, obj):
        url = reverse('order:change-order-paid', args=[obj.id])
        return url

    def get_public_link(self, obj):
        return obj.get_id_link()

    def get_create_time_display(self, obj):
        return obj.create_time.strftime('%m-%d')

    def get_product_summary(self, obj):
        return obj.get_product_summary()


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
