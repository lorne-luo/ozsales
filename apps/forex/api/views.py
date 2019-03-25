from rest_framework import permissions
from core.api.views import CommonViewSet
from ..models import Store, Page
from . import serializers


# class PageViewSet(CommonViewSet):
#     """ api views for Page """
#     queryset = Page.objects.all()
#     serializer_class = serializers.PageSerializer
#     filter_fields = ['title', 'url', 'store']
#     search_fields = ['title', 'url', 'store']

