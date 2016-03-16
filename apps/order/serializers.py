# coding=utf-8
from django.core.urlresolvers import reverse
from rest_framework import serializers
from models import Order, ORDER_STATUS


# Serializer for order
class OrderSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    customer_display = serializers.CharField(source='customer')
    status_button = serializers.SerializerMethodField()
    customer_url = serializers.SerializerMethodField()
    shipping_order = serializers.SerializerMethodField()
    paid_url = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['link'] + ['customer', 'customer_display', 'address', 'is_paid', 'status', 'total_amount',
                             'product_cost_aud', 'customer_url', 'shipping_order', 'status_button', 'paid_url',
                             'product_cost_rmb', 'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb',
                             'origin_sell_rmb', 'sell_price_rmb', 'profit_rmb', 'create_time', 'finish_time'] + ['id']
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

    def get_customer_url(self, obj):
        url = reverse('admin:customer_customer_change', args=[obj.customer.id])
        return url

    def get_shipping_order(self, obj):
        return obj.get_shipping_orders()

    def get_status_button(self, obj):
        current_status = ''
        if obj.status in [ORDER_STATUS.CREATED, ORDER_STATUS.DELIVERED]:
            current_status += '<b>%s</b>' % obj.status
        else:
            current_status += obj.status

        next_status = obj.next_status
        if not next_status:
            return ORDER_STATUS.FINISHED

        btn = '%s<br/> => <a href="%s">%s</a>' % (current_status, url, next_status)
        url = reverse('order:change-order-status', kwargs={'order_id': obj.id, 'status_value': next_status})
        return btn

    def get_paid_url(self, obj):
        url = reverse('order:change-order-paid', args=[obj.id])
        return url
