from django.core.urlresolvers import reverse
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    edit_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = None

    def get_detail_url(self, obj):
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name

        if self.has_perm('view'):
            url_tag = '%s:%s-detail' % (app_label, model_name)
            return reverse(url_tag, args=[obj.id])
        return None

    def get_edit_url(self, obj):
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name

        if self.has_perm('change'):
            url_tag = '%s:%s-update' % (app_label, model_name)
            return reverse(url_tag, args=[obj.id])
        elif self.has_perm('view'):
            return self.get_detail_url(obj)
        return None

    def has_perm(self, perm):
        user = self.context['request'].user
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name
        perm_str = '%s.%s_%s' % (app_label, perm, model_name)
        return user.has_perm(perm_str)


class SellerOwnerSerializerMixin(object):
    def get_is_owner(self, obj):
        request = self.context.get("request")
        if not obj.seller and request.user.is_superuser:
            return True
        return obj.seller == request.profile
