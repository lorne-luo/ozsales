# coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from views import CommonListPageView, \
    CommonCreatePageView, CommonUpdatePageView, CommonDeletePageView, \
    CommonDetailPageView

urlpatterns = [
    # for page
    url(r'/403.html', TemplateView.as_view(template_name='adminlte/403.html'),
        name='http403'),

    url(r'common/(?P<app_name>\w+)/(?P<model_name>\w+)/list/$',
        login_required(CommonListPageView.as_view()),
        name='common_list_page'),

    url(r'common/(?P<app_name>\w+)/(?P<model_name>\w+)/create/$',
        login_required(CommonCreatePageView.as_view()),
        name='common_create_page'),

    url(r'common/(?P<app_name>\w+)/(?P<model_name>\w+)/detail/(?P<pk>\d+)/$',
        login_required(CommonDetailPageView.as_view()),
        name='common_detail_page'),

    url(r'common/(?P<app_name>\w+)/(?P<model_name>\w+)/update/(?P<pk>\d+)/$',
        login_required(CommonUpdatePageView.as_view()),
        name='common_update_page'),

    url(r'common/(?P<app_name>\w+)/(?P<model_name>\w+)/delete/$',
        login_required(CommonDeletePageView.as_view()),
        name='common_delete_page'),
]
