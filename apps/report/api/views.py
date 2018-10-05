# coding=utf-8
from core.api.views import CommonViewSet
from ..models import MonthlyReport
from . import serializers


class MonthlyReportViewSet(CommonViewSet):
    """ API views for MonthlyReport """
    queryset = MonthlyReport.objects.all()
    serializer_class = serializers.MonthlyReportSerializer
    filter_fields = []
    search_fields = []
