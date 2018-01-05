# coding=utf-8
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework import permissions

from core.api.views import CommonViewSet
from ..models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task
from . import serializers


@login_required
@require_http_methods(["POST"])
def sitemail_markall(request):
    SiteMailReceive.objects.exclude(
        status=SiteMailReceive.DELETED
    ).filter(receiver=request.user).update(status=SiteMailReceive.READ)
    return JsonResponse({'message': u'ok'}, status=200)


class NotificationViewSet(CommonViewSet):
    """ api views for Notification """
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'content', 'receiver', 'status', 'read_time', 'creator']
    search_fields = ['title', 'content', 'receiver', 'status', 'read_time', 'creator']


class NotificationContentViewSet(CommonViewSet):
    """ api views for NotificationContent """
    queryset = NotificationContent.objects.all()
    serializer_class = serializers.NotificationContentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'contents', 'status', 'creator']
    search_fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentViewSet(CommonViewSet):
    """ api views for SiteMailContent """
    queryset = SiteMailContent.objects.all()
    serializer_class = serializers.SiteMailContentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'contents', 'status', 'creator']
    search_fields = ['title', 'contents', 'status', 'creator']


class SiteMailReceiveViewSet(CommonViewSet):
    """ api views for SiteMailReceive """
    queryset = SiteMailReceive.objects.all()
    serializer_class = serializers.SiteMailReceiveSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'content__contents', 'status', 'sender__seller__name', 'creator__seller__name',
                     'receiver__seller__name']
    search_fields = ['title', 'content__contents', 'status', 'sender__seller__name', 'creator__seller__name',
                     'receiver__seller__name']

    def get_queryset(self):
        queryset = super(SiteMailReceiveViewSet, self).get_queryset()
        return queryset.filter(receiver=self.request.user)


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
