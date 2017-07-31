# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api.routers import PostHackedRouter
import views


urlpatterns = []
router = PostHackedRouter()
router.include_root_view = False

# urls for monthlyreport
urlpatterns += patterns('',
    #url(r'^report/monthlyreport/add/$', login_required(views.MonthlyReportAddView.as_view()), name='monthlyreport-add'),
    url(r'^report/monthlyreport/list/$', login_required(views.MonthlyReportListView.as_view()), name='monthlyreport-list'),
    url(r'^report/monthlyreport/(?P<pk>\d+)/$', login_required(views.MonthlyReportDetailView.as_view()), name='monthlyreport-detail'),
    url(r'^report/monthlyreport/(?P<pk>\d+)/edit/$', login_required(views.MonthlyReportUpdateView.as_view()), name='monthlyreport-update'),
    url(r'^report/total_report/$', views.TotalReport.as_view(),name='total-report'),
)


# reverse('report:api-monthlyreport-list'), reverse('report:api-monthlyreport-detail', kwargs={'pk': 1})
router.register(r'api/report/monthlyreport', views.MonthlyReportViewSet, base_name='api-monthlyreport')


urlpatterns += router.urls
