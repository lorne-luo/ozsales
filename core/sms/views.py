# coding=utf-8

import urllib
from utils.telstra_api import MessageSender
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny


def sms_send(request):
    m = MessageSender()
    m.send_to_self('hello boy')

    return Response({'success': True})


class SMSSender(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        body = self.request.query_params.get('body', '')
        to = self.request.query_params.get('to', '')
        if body and to:
            m = MessageSender()
            m.send_sms(to, body)
            return Response({'success': True})
        else:
            return Response({'success': False})


class SMSSelfSender(SMSSender):
    def get(self, request, *args, **kwargs):
        body = self.request.query_params.get('body', '')
        if body:
            m = MessageSender()
            m.send_to_self(body)
            return Response({'success': True})
        else:
            return Response({'success': False})
