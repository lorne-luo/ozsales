# coding=utf-8

import urllib
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from utils.telstra_api import MessageSender


def sms_send(request):
    m = MessageSender()
    m.send_to_self('hello boy')

    return Response({'success': True})


class SMSSender(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.call_send_sms()

    def call_send_sms(self):
        body = self.request.query_params.get('body', '')
        to = self.request.query_params.get('to', '')
        if body and to:
            m = MessageSender()
            result, detail = m.send_sms(to, body)
            return Response({'success': result, 'detail': detail})
        return Response({'success': False, 'detail': 'to or body is null'})


class SMSSelfSender(SMSSender):
    def call_send_sms(self):
        body = self.request.query_params.get('body', '')
        if body:
            m = MessageSender()
            result, detail = m.send_to_self(body)
            return Response({'success': result, 'detail': detail})
        return Response({'success': False, 'detail': 'body is null'})


def sms_record(request):
    handle=open(MessageSender.SMS_TXT_PATH, 'r')
    sms_records = handle.read()
    handle.close()
    return HttpResponse(sms_records, content_type="text/plain")