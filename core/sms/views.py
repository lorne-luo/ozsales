# coding=utf-8

import sys
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ViewDoesNotExist, ObjectDoesNotExist
from django.http import Http404
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

    def post(self, request, *args, **kwargs):
        content = self.request.query_params.get('content', '')
        to = self.request.query_params.get('to', '')
        if content and to:
            m = MessageSender()
            m.send_sms(to, content)
            return Response({'success': True})
        else:
            return Response({'success': False})


class SMSSelfSender(SMSSender):
    def post(self, request, *args, **kwargs):
        content = self.request.query_params.get('content', '')
        if content:
            m = MessageSender()
            m.send_to_self(content)
            return Response({'success': True})
        else:
            return Response({'success': False})
