# coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import CommonListCreateAPIView, CommonRetrieveUpdateAPIView

urlpatterns = [
    # common api for all models
    url(r'(?P<app_name>\w+)/(?P<model_name>\w+)/(?P<pk>\d+)$',
        CommonRetrieveUpdateAPIView.as_view(), name='retriveupdate_api'),

    url(r'(?P<app_name>\w+)/(?P<model_name>\w+)/$',
        CommonListCreateAPIView.as_view(), name='listcreate_api'),
]
