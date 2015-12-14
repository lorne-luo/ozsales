# coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView

from .views_api import CommonListCreateAPIView, CommonRetrieveUpdateAPIView
from .views import CommonListPageView, \
    CommonCreatePageView, CommonUpdatePageView, CommonDeletePageView, \
    CommonDetailPageView

urlpatterns = [
    # for page
    url(r'/403.html', TemplateView.as_view(template_name='adminlte/403.html'),
        name='http403'),

    url(r'/(?P<app_name>\w+)/(?P<model_name>\w+)/list$',
        CommonListPageView.as_view(),
        name='common_list_page'),

    url(r'/(?P<app_name>\w+)/(?P<model_name>\w+)/create$',
        CommonCreatePageView.as_view(),
        name='common_create_page'),

    url(r'/(?P<app_name>\w+)/(?P<model_name>\w+)/detail/(?P<pk>\d+)$',
        CommonDetailPageView.as_view(),
        name='common_detail_page'),

    url(r'/(?P<app_name>\w+)/(?P<model_name>\w+)/update/(?P<pk>\d+)$',
        CommonUpdatePageView.as_view(),
        name='common_update_page'),

    url(r'/(?P<app_name>\w+)/(?P<model_name>\w+)/delete$',
        CommonDeletePageView.as_view(),
        name='common_delete_page'),

    # for api
    url(r'api/v2/(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<pk>\d+)$',
        CommonRetrieveUpdateAPIView.as_view(), name='common_retriveupdate_api'),

    url(r'api/v2/(?P<app_name>\w+)/(?P<model_name>\w+)/$',
        CommonListCreateAPIView.as_view(), name='common_listcreate_api'),
]
