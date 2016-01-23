# coding=utf-8
from rest_framework import serializers
from .models import Product


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
            img = '/media/no_image.gif'
        return '<a href="%s" target="_blank"><img style="height:60px" src="%s"/></a>' % (img, img)

