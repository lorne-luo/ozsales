from rest_framework import serializers
from core.api.serializers import BaseSerializer
from apps.report.models import MonthlyReport


class MonthlyReportSerializer(BaseSerializer):
    """ Serializer for MonthlyReport """
    month = serializers.DateField(format='%Y-%m', input_formats=None)
    cost_aud = serializers.IntegerField()
    cost_rmb = serializers.IntegerField()
    shipping_fee = serializers.IntegerField()
    sell_price_rmb = serializers.IntegerField()
    profit_rmb = serializers.IntegerField()

    class Meta:
        model = MonthlyReport
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['month', 'order_count', 'parcel_count', 'cost_aud', 'cost_rmb', 'shipping_fee', 'sell_price_rmb',
                  'profit_rmb']
        read_only_fields = ['id']
