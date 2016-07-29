# coding=utf-8
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import SMSSender, SMSSelfSender, sms_record

urlpatterns = [
    # common api for all models
    url(r'api/sms/send/$', SMSSender.as_view(), name='sms_send'),
    url(r'api/sms/send/self/$', SMSSelfSender.as_view(), name='sms_send_self'),
    url(r'^sms/$', sms_record, name="sms_record"),
]
