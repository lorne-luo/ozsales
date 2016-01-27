SERIALIZERS_HEADER = '''
from django.core.urlresolvers import reverse
from rest_framework import serializers
'''

SERIALIZERS_MODEL_TEMPLATE = '''
from models import <% MODEL_NAME %>

class <% MODEL_NAME %>Serializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = <% MODEL_NAME %>
        fields = <% fields %>
        read_only_fields = ['id']

    def get_link(self, obj):
        request = self.context.get('request', None)

        change_perm_str = '%s.change_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        view_perm_str = '%s.view_%s' % (self.Meta.model._meta.app_label, self.Meta.model._meta.model_name)
        if request.user.has_perm(change_perm_str):
            url = reverse('<% model_name %>-update', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Update Link')
        elif request.user.has_perm(view_perm_str):
            url = reverse('<% model_name %>-detail', args=[obj.id])
            return '<a href="%s">%s</a>' % (url, 'Detail Link')
        return None
'''
