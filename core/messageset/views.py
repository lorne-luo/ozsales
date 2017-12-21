# coding=utf-8
from braces.views import MultiplePermissionsRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework import permissions
from models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task, \
    create_sitemail_datas
import serializers
import forms
import serializers
from core.django.views import CommonContextMixin
from core.api.views import CommonViewSet
from models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task


@login_required
@require_http_methods(["POST"])
def sitemail_markall(request):
    SiteMailReceive.objects.exclude(
        status=SiteMailReceive.DELETED
    ).filter(receiver=request.user).update(status=SiteMailReceive.READ)
    return JsonResponse({'message': u'ok'}, status=200)


# views for Notification

class NotificationListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Notification
    template_name_suffix = '_list'  # notification/notification_list.html
    permissions = {
        "all": ("messageset.view_notification",)
    }

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        context['table_titles'] = [u'标题', u'内容', u'状态']
        context['table_fields'] = ['link', 'content', 'status']
        return context


class NotificationUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Notification
    form_class = forms.NotificationUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("notification.change_notification",)
    }


class NotificationDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Notification
    form_class = forms.NotificationDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("notification.view_notification",)
    }


# api views for Notification

class NotificationViewSet(CommonViewSet):
    queryset = Notification.objects.all()
    serializer_class = serializers.NotificationSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'content', 'receiver', 'status', 'read_time', 'creator']
    search_fields = ['title', 'content', 'receiver', 'status', 'read_time', 'creator']


class NotificationContentAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = NotificationContent
    form_class = forms.NotificationContentAddForm
    template_name = 'messageset/notificationcontent_form.html'
    permissions = {
        "all": ("notificationcontent.add_notificationcontent",)
    }

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = notification_content = form.save(commit=False)
            notification_content.creator = request.user
            notification_content.save()
            return HttpResponseRedirect(self.get_success_url())
        else:

            return self.form_invalid(form)


class NotificationContentUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = NotificationContent
    form_class = forms.NotificationContentUpdateForm
    template_name = 'messageset/notificationcontent_form.html'
    permissions = {
        "all": ("notificationcontent.change_notificationcontent",)
    }


class NotificationContentDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = NotificationContent
    form_class = forms.NotificationContentDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("notificationcontent.view_notificationcontent",)
    }


# api views for NotificationContent

class NotificationContentViewSet(CommonViewSet):
    queryset = NotificationContent.objects.all()
    serializer_class = serializers.NotificationContentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'contents', 'status', 'creator']
    search_fields = ['title', 'contents', 'status', 'creator']


# views for SiteMailContent
class SiteMailContentAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = SiteMailContent
    form_class = forms.SiteMailContentAddForm
    template_name = 'messageset/sitemail_form.html'
    permissions = {
        "all": ("sitemailcontent.add_sitemailcontent",)
    }

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            sitemail = form.save(commit=False)
            sitemail.creator = request.user
            post_save.disconnect(create_sitemail_datas, sender=SiteMailContent)
            sitemail.save()
            #fixme not correctly create SiteMailReceive
            sitemail.receivers = form.cleaned_data['receivers']
            post_save.connect(create_sitemail_datas, sender=SiteMailContent)
            sitemail.save()
            return redirect('messageset:sitemail-list')
        else:

            return self.form_invalid(form)


class SiteMailContentUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = SiteMailContent
    form_class = forms.SiteMailContentUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("sitemailcontent.change_sitemailcontent",)
    }


class SiteMailContentDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = SiteMailContent
    form_class = forms.SiteMailContentDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("sitemailcontent.view_sitemailcontent",)
    }


# api views for SiteMailContent

class SiteMailContentViewSet(CommonViewSet):
    queryset = SiteMailContent.objects.all()
    serializer_class = serializers.SiteMailContentSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'contents', 'status', 'creator']
    search_fields = ['title', 'contents', 'status', 'creator']


# views for SiteMailReceive

class SiteMailReceiveListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = SiteMailReceive
    template_name_suffix = '_list'  # sitemailreceive/sitemailreceive_list.html
    permissions = {
        "all": ("messageset.view_sitemailreceive",)
    }

    def get_context_data(self, **kwargs):
        context = super(SiteMailReceiveListView, self).get_context_data(**kwargs)
        context['table_titles'] = [u'主题', u'发件人', u'读取状态', u'收件时间'] + ['']
        context['table_fields'] = ['title', 'sender', 'status', 'send_time'] + ['id']
        return context


class SiteMailReceiveDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = SiteMailReceive
    form_class = forms.SiteMailReceiveDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("sitemailreceive.view_sitemailreceive",)
    }


# api views for SiteMailReceive

class SiteMailReceiveViewSet(CommonViewSet):
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


# views for SiteMailSend
class SiteMailSendDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = SiteMailSend
    form_class = forms.SiteMailSendDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("sitemailsend.view_sitemailsend",)
    }


# api views for SiteMailSend

class SiteMailSendViewSet(CommonViewSet):
    queryset = SiteMailSend.objects.all()
    serializer_class = serializers.SiteMailSendSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'content', 'sender', 'status', 'creator']
    search_fields = ['title', 'content', 'sender', 'status', 'creator']


# views for Task

class TaskListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Task
    template_name_suffix = '_list'  # task/task_list.html
    permissions = {
        "all": ("messageset.view_task",)
    }

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['table_titles'] = [u'名称', u'状态', u'进度', u'开始时间']
        context['table_fields'] = ['link', 'status', 'percent', 'start_time']
        return context


class TaskDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Task
    form_class = forms.TaskDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("task.view_task",)
    }


# api views for Task

class TaskViewSet(CommonViewSet):
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['name', 'start_app', 'status']
    search_fields = ['name', 'start_app', 'status']
