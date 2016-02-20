# coding=utf-8
from rest_framework import serializers
from django.core.urlresolvers import reverse
from models import Product, Brand


class ProductSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    brand = serializers.CharField()
    pic = serializers.SerializerMethodField('get_pic_link')

    class Meta:
        model = Product
        fields = Product.Config.list_display_fields + ('id', 'link')
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)
        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            return obj.get_edit_link()
        elif request.user.has_perm(view_perm_str):
            return obj.get_detail_link()
        return obj.name_cn

    def get_pic_link(self, obj):
        if obj.pic:
            img = '%s' % obj.pic.url
        else:
            img = '/static/img/no_image.jpg'
        return '<a href="%s" target="_blank"><img style="height:90px" src="%s"/></a>' % (img, img)


# Serializer for brand
class BrandSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['link'] + ['name_en', 'name_cn', 'country', 'remarks'] + ['id']
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            url = reverse('product:brand-update', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Update Link')
        elif request.user.has_perm(view_perm_str):
            url = reverse('product:brand-detail', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Detail Link')
        return None
