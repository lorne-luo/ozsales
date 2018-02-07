# coding=utf-8
from core.api.views import CommonViewSet
from core.auth_user.views import OwnerViewSetMixin
from ..models import MonthlyReport
from . import serializers


class MonthlyReportViewSet(OwnerViewSetMixin, CommonViewSet):
    """ API views for MonthlyReport """
    queryset = MonthlyReport.objects.all()
    serializer_class = serializers.MonthlyReportSerializer
    filter_fields = []
    search_fields = []
