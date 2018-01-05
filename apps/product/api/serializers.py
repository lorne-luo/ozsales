from rest_framework import serializers
from core.api.serializers import BaseSerializer
from ..models import Product, Brand


class ProductSerializer(BaseSerializer):
    """Serializer for product"""
    brand_display = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name_en', 'name_cn', 'pic', 'brand_cn', 'brand_en', 'brand_display', 'spec', 'max_cost',
                  'last_sell_price', 'avg_sell_price', 'min_sell_price', 'max_sell_price', 'avg_cost', 'min_cost']
        read_only_fields = ['id']

    def get_pic_link(self, obj):
        if obj.pic:
            img = '%s' % obj.pic.url
        else:
            img = '/static/img/no_image.jpg'
        return '<a href="%s" target="_blank"><img style="height:90px" src="%s"/></a>' % (img, img)

    def get_brand_display(self, obj):
        return str(obj.brand)


class BrandSerializer(BaseSerializer):
    """ Serializer for Brand """

    class Meta:
        model = Brand
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name_en', 'name_cn', 'short_name', 'remarks']
        read_only_fields = ['id']
