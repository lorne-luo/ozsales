# coding=utf-8
from django.core.urlresolvers import reverse
from rest_framework import serializers
from core.api.serializers import BaseSerializer
from models import Product, Brand


# Serializer for product
class ProductSerializer(BaseSerializer):
    brand_display = serializers.CharField(source='brand')

    class Meta:
        model = Product
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name_en', 'name_cn', 'pic', 'brand', 'brand_display', 'spec1', 'spec2', 'spec3', 'normal_price',
                  'bargain_price', 'safe_sell_price', 'tb_url', 'wd_url', 'wx_url']
        read_only_fields = ['id']

    def get_pic_link(self, obj):
        if obj.pic:
            img = '%s' % obj.pic.url
        else:
            img = '/static/img/no_image.jpg'
        return '<a href="%s" target="_blank"><img style="height:90px" src="%s"/></a>' % (img, img)


class BrandSerializer(BaseSerializer):
    """ Serializer for Brand """

    class Meta:
        model = Brand
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['name_en', 'name_cn', 'country', 'short_name', 'remarks', 'category']
        read_only_fields = ['id']
