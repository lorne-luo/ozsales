# coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import SMSSender, SMSSelfSender

urlpatterns = [
    # common api for all models
    url(r'sms/send/$', SMSSender.as_view(), name='sms_send'),
    url(r'sms/send/self/$', SMSSelfSender.as_view(), name='sms_send_self'),
]
