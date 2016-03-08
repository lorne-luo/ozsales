# coding=utf-8
from django.core.urlresolvers import reverse
from rest_framework import serializers
from models import Order


# Serializer for order
class OrderSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['link'] + ['customer', 'address', 'is_paid', 'status', 'total_amount', 'product_cost_aud',
                             'product_cost_rmb', 'shipping_fee', 'ship_time', 'total_cost_aud', 'total_cost_rmb',
                             'origin_sell_rmb', 'sell_price_rmb', 'profit_rmb', 'finish_time'] + ['id']
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        name = u'[%s]%s' % (obj.id, obj.customer)
        if request.user.has_perm(change_perm_str):
            url = reverse('order:order-detail-short', args=[obj.customer.id, obj.id])
            return u'<a href="%s">%s</a>' % (url, name)
        elif request.user.has_perm(view_perm_str):
            url = reverse('order:order-detail-short', args=[obj.customer.id, obj.id])
            return u'<a href="%s">%s</a>' % (url, name)
        return name

