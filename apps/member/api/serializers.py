from rest_framework import serializers
from ..models import Seller


class SellerSerializer(serializers.ModelSerializer):
    ''' Serializer for class Seller '''
    groups = serializers.SerializerMethodField()
    groups_display = serializers.SerializerMethodField()

    class Meta:
        model = Seller
        fields = ['pk', 'country', 'auth_user', 'name', 'expire_at', 'start_at', 'groups', 'groups_display']

    def get_groups_display(self, obj):
        if obj.auth_user:
            return [x.name for x in obj.auth_user.groups.all()]
        else:
            return []

    def get_groups(self, obj):
        if obj.auth_user:
            return [x.pk for x in obj.auth_user.groups.all()]
        else:
            return []
