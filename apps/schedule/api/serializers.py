from core.api.serializers import BaseSerializer
from ..models import DealSubscribe


class DealSubscribeSerializer(BaseSerializer):
    """ Serializer for DealSubscribe """

    class Meta:
        model = DealSubscribe
        fields = ['id', 'edit_url', 'detail_url'] + \
                 ['includes', 'excludes', 'is_active']
        read_only_fields = ['id']