# coding=utf-8
from rest_framework.generics import GenericAPIView
from django.http import HttpResponse
from rest_framework.response import Response

from core.api.permission import AdminOnlyPermissions
from .telstra_api import MessageSender
from .models import Sms


class SMSSender(GenericAPIView):
    permission_classes = [AdminOnlyPermissions]

    def get(self, request, *args, **kwargs):
        return self.call_send_sms()

    def call_send_sms(self):
        body = self.request.query_params.get('body', '')
        to = self.request.query_params.get('to', '')
        app_name = self.request.query_params.get('app_name', None)
        if body and to:
            m = MessageSender()
            result, detail = m.send_sms(to, body, app_name)
            return Response({'success': result, 'detail': detail})
        return Response({'success': False, 'detail': 'to or body is null'})


class SMSSelfSender(SMSSender):
    def call_send_sms(self):
        body = self.request.query_params.get('body', '')
        app_name = self.request.query_params.get('app_name', None)
        if body:
            m = MessageSender()
            result, detail = m.send_to_admin(body, app_name)
            return Response({'success': result, 'detail': detail})
        return Response({'success': False, 'detail': 'body is null'})


def sms_record(request):
    sms_list = Sms.objects.all().order_by('-id')[:20]
    sms_records = ''
    for sms in sms_list:
        sms_records += '[%s] %s | %s\n\n' % (sms.time.strftime("%Y-%m-%d %H:%M:%S"), sms.send_to, sms.content)
    return HttpResponse(sms_records, content_type="text/plain")
