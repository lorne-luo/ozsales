from django.core.urlresolvers import reverse
from rest_framework import serializers
from models import Page, Store


# Serializer for page
class PageSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['link'] + ['title', 'url', 'store', 'price', 'original_price'] + ['id']
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            url = reverse('store:page-update', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Update Link')
        elif request.user.has_perm(view_perm_str):
            url = reverse('store:page-detail', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Detail Link')
        return None


# Serializer for store
class StoreSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['link'] + ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate'] + ['id']
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            url = reverse('store:store-update', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Update Link')
        elif request.user.has_perm(view_perm_str):
            url = reverse('store:store-detail', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Detail Link')
        return None

