# coding=utf-8
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    primary_address = serializers.CharField()
    name = serializers.SerializerMethodField('get_link')

    class Meta:
        model = Customer
        fields = Customer.Config.list_display_fields + ('id',)
        read_only_fields = (
            'id', 'date_joined'
        )

    def get_link(self, obj):
        request = self.context.get('request', None)
        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            return obj.get_edit_link()
        elif request.user.has_perm(view_perm_str):
            return obj.get_detail_link()
        return obj.name
