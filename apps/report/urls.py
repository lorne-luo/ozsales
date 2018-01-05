# coding=utf-8
from django.conf.urls import url
from . import views

# urls for monthlyreport
urlpatterns = (
    url(r'^monthlyreport/list/$', views.MonthlyReportListView.as_view(), name='monthlyreport-list'),
    url(r'^monthlyreport/(?P<pk>\d+)/$', views.MonthlyReportDetailView.as_view(), name='monthlyreport-detail'),
    url(r'^monthlyreport/(?P<pk>\d+)/edit/$', views.MonthlyReportUpdateView.as_view(), name='monthlyreport-update'),
)
