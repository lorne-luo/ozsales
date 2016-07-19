from django.core.urlresolvers import reverse
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    edit_url = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = None

    def get_detail_url(self, obj):
        user = self.context['request'].user
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name

        view_perm_str = '%s.view_%s' % (app_label, model_name)
        if user.has_perm(view_perm_str):
            url_tag = '%s:%s-detail' % (app_label, model_name)
            return reverse(url_tag, args=[obj.id])
        return None

    def get_edit_url(self, obj):
        user = self.context['request'].user
        app_label = self.Meta.model._meta.app_label
        model_name = self.Meta.model._meta.model_name

        change_perm_str = '%s.change_%s' % (app_label, model_name)
        view_perm_str = '%s.view_%s' % (app_label, model_name)
        if user.has_perm(change_perm_str):
            url_tag = '%s:%s-update' % (app_label, model_name)
            return reverse(url_tag, args=[obj.id])
        elif user.has_perm(view_perm_str):
            url_tag = '%s:%s-detail' % (app_label, model_name)
            return reverse(url_tag, args=[obj.id])
        return None
