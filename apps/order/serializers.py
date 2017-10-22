# coding=utf-8
from django.core.urlresolvers import reverse
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from models import OrderProduct, Order, ORDER_STATUS, ORDER_STATUS_CHOICES


class OrderProductSerializer(BaseSerializer):
    """ Serializer for OrderProduct """
    order_display = serializers.StringRelatedField(source='order', read_only=True)
    store_display = serializers.StringRelatedField(source='store', read_only=True)
    order_url = serializers.SerializerMethodField()
    product_url = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = ['id', 'detail_url'] + \
                 ['order', 'product', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud',
                  'total_price_aud', 'store', 'order_display', 'order_url', 'product_url', 'store_display',
                  'is_purchased']
        read_only_fields = ['id']

    def get_order_url(self, obj):
        user = self.context['request'].user

        if user.has_perm('order.change_order'):
            url_tag = 'order:order-update'
            return reverse(url_tag, args=[obj.order.id])
        elif user.has_perm('order.view_order'):
            url_tag = 'order:order-detail'
            return reverse(url_tag, args=[obj.order.id])
        return None

    def get_product_url(self, obj):
        user = self.context['request'].user

        if obj.product:
            if user.has_perm('product.change_product'):
                url_tag = 'product:product-update'
                return reverse(url_tag, args=[obj.product.id])
            elif user.has_perm('product.view_product'):
                url_tag = 'product:product-detail'
                return reverse(url_tag, args=[obj.product.id])
        return None


class OrderProductDisplaySerializer(OrderProductSerializer):
    sell_price_rmb = serializers.IntegerField()

    class Meta:
        model = OrderProduct
        fields = ['id', 'name', 'amount', 'sell_price_rmb', 'total_price_rmb', 'cost_price_aud', 'total_price_aud',
                  'is_purchased']


class OrderSerializer(BaseSerializer):
    """ Serializer for Order """
    address_display = serializers.CharField(source='address')
    customer_display = serializers.CharField(source='customer')
    customer_url = serializers.SerializerMethodField()
    shipping_order = serializers.SerializerMethodField()
    paid_url = serializers.SerializerMethodField()
    public_link = serializers.SerializerMethodField()
    create_time = serializers.DateTimeField(format='%m-%d', input_formats=None)
    next_status_url = serializers.SerializerMethodField()
    next_status = serializers.SerializerMethodField()
    product_summary = serializers.SerializerMethodField()
    sell_price_rmb = serializers.IntegerField()
    shipping_fee = serializers.IntegerField()
    total_cost_aud = serializers.IntegerField()
    total_cost_rmb = serializers.IntegerField()
    profit_rmb = serializers.IntegerField()
    products = OrderProductDisplaySerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'customer_display', 'address', 'is_paid', 'status', 'total_amount', 'public_link',
                  'product_cost_aud', 'customer_url', 'shipping_order', 'paid_url', 'next_status_url', 'next_status',
                  'product_summary', 'address_display', 'detail_url',
                  'product_cost_rmb', 'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb', 'edit_url',
                  'origin_sell_rmb', 'sell_price_rmb', 'profit_rmb', 'create_time', 'finish_time', 'id', 'products']
        read_only_fields = ['id']

    def get_detail_url(self, obj):
        return reverse('order:order-detail-short', args=[obj.customer.id, obj.id])

    def get_customer_url(self, obj):
        user = self.context['request'].user
        if user.has_perm('customer.change_customer'):
            return reverse('customer:customer-update', args=[obj.customer.id])
        elif user.has_perm('customer.view_customer'):
            return reverse('customer:customer-detail', args=[obj.customer.id])
        return None

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

    def get_product_summary(self, obj):
        return obj.get_product_summary()
