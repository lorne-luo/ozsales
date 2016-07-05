from django.shortcuts import render

from rest_framework import permissions
from core.adminlte.views import CommonContextMixin, CommonViewSet
from .models import ExpressOrder
import serializers
from django_filters import Filter, FilterSet


class ExpressOrderViewSet(CommonViewSet):
    """ api views for ExpressOrder """
    serializer_class = serializers.ExpressOrderSerializer
    # filter_class = OrderFilter
    permission_classes = [permissions.DjangoModelPermissions]
    search_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']

    def get_queryset(self):
        return ExpressOrder.objects.all()
