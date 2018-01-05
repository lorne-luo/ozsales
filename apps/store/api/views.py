from rest_framework import permissions
from core.api.views import CommonViewSet
from ..models import Store, Page
from . import serializers


class PageViewSet(CommonViewSet):
    """ api views for Page """
    queryset = Page.objects.all()
    serializer_class = serializers.PageSerializer
    filter_fields = ['id']
    search_fields = ['title', 'url', 'store', 'price', 'original_price']


class StoreViewSet(CommonViewSet):
    """ api views for Store """
    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['id']
    search_fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']
