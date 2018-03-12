# coding=utf-8
from collections import OrderedDict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from core.api.pagination import CommonPageNumberPagination
from core.api.views import CommonViewSet
from core.django.constants import MailStatus
from ..models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task
from . import serializers


@login_required
@require_http_methods(["POST"])
def sitemail_markall(request):
    SiteMailReceive.objects.exclude(
        status=SiteMailReceive.DELETED
    ).filter(receiver=request.user).update(status=SiteMailReceive.READ)
    return JsonResponse({'message': u'ok'}, status=200)


@login_required
@require_http_methods(["POST"])
def notification_markall(request):
    Notification.objects.exclude(
        status=Notification.DELETED
    ).filter(receiver=request.user).update(status=Notification.READ)
    return JsonResponse({'message': u'ok'}, status=200)


class OwnerMessageViewSetMixin(object):
    """some model use receivers, diff with below one"""

    def get_queryset(self):
        queryset = super(OwnerMessageViewSetMixin, self).get_queryset()
        return queryset.filter(receivers=self.request.user)


class OwnerMessageViewSetMixin2(object):
    """some model use receiver"""

    def get_queryset(self):
        queryset = super(OwnerMessageViewSetMixin2, self).get_queryset()
        return queryset.filter(receiver=self.request.user)


class NotificationPaginator(CommonPageNumberPagination):
    page_size = 10


class NotificationViewSet(OwnerMessageViewSetMixin2, CommonViewSet):
    """ api views for Notification """
    queryset = Notification.objects.filter(status__lt=MailStatus.DRAFT)
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'status']
    search_fields = ['title', 'status']
    ordering_fields = ['id', 'send_time', 'status']
    pagination_class = NotificationPaginator

    def get_paginated_response(self, data):
        response = super(NotificationViewSet, self).get_paginated_response(data)
        response.data.update({
            'unread_count': Notification.objects.filter(receiver=self.request.user,
                                                        status=Notification.UNREAD).count()
        })
        return response


class NotificationContentViewSet(OwnerMessageViewSetMixin, CommonViewSet):
    """ api views for NotificationContent """
    queryset = NotificationContent.objects.all()
    serializer_class = serializers.NotificationContentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'contents', 'status', 'creator']
    search_fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentViewSet(OwnerMessageViewSetMixin, CommonViewSet):
    """ api views for SiteMailContent """
    queryset = SiteMailContent.objects.all()
    serializer_class = serializers.SiteMailContentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'contents', 'status', 'creator']
    search_fields = ['title', 'contents', 'status', 'creator']


class SiteMailReceiveViewSet(OwnerMessageViewSetMixin2, CommonViewSet):
    """ api views for SiteMailReceive """
    queryset = SiteMailReceive.objects.all()
    serializer_class = serializers.SiteMailReceiveSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'content__contents', 'status', 'sender__seller__name', 'creator__seller__name',
                     'receiver__seller__name']
    search_fields = ['title', 'content__contents', 'status', 'sender__seller__name', 'creator__seller__name',
                     'receiver__seller__name']
    ordering_fields = ['id', 'send_time']

    def get_paginated_response(self, data):
        response = super(SiteMailReceiveViewSet, self).get_paginated_response(data)
        response.data.update({
            'unread_count': SiteMailReceive.objects.filter(receiver=self.request.user,
                                                           status=SiteMailReceive.UNREAD).count()
        })
        return response


class SiteMailSendViewSet(CommonViewSet):
    """ api views for SiteMailSend """
    queryset = SiteMailSend.objects.all()
    serializer_class = serializers.SiteMailSendSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'content', 'sender', 'status', 'creator']
    search_fields = ['title', 'content', 'sender', 'status', 'creator']


class TaskViewSet(CommonViewSet):
    """ api views for Task """
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['name', 'start_app', 'status']
    search_fields = ['name', 'start_app', 'status']
    ordering_fields = ['id', 'start_time', 'status']
