# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from core.adminlte.views import CommonContextMixin, CommonViewSet
from models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task
import serializers
import forms


@login_required
@require_http_methods(["PATCH"])
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
        context['table_titles'] = ['Link'] + [u'标题', u'内容', u'接收人', u'读取状态', u'读取时间', u'数据创建人', u'数据删除时间'] + ['']
        context['table_fields'] = ['link'] + ['title', 'content', 'receiver', 'status', 'read_time', 'creator', 'deleted_at'] + ['id']
        return context


class NotificationAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Notification
    form_class = forms.NotificationAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("notification.add_notification",)
    }

    def get_success_url(self):
        return reverse('messageset:notification-list')


class NotificationUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Notification
    form_class = forms.NotificationUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("notification.change_notification",)
    }

    def get_success_url(self):
        return reverse('messageset:notification-list')


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


# views for NotificationContent

class NotificationContentListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = NotificationContent
    template_name_suffix = '_list'  # notificationcontent/notificationcontent_list.html
    permissions = {
        "all": ("messageset.view_notificationcontent",)
    }

    def get_context_data(self, **kwargs):
        context = super(NotificationContentListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Link'] + [u'标题', u'内容', u'状态', u'数据创建人', u'数据删除时间'] + ['']
        context['table_fields'] = ['link'] + ['title', 'contents', 'status', 'creator', 'deleted_at'] + ['id']
        return context


class NotificationContentAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = NotificationContent
    form_class = forms.NotificationContentAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("notificationcontent.add_notificationcontent",)
    }

    def get_success_url(self):
        return reverse('messageset:notificationcontent-list')


class NotificationContentUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = NotificationContent
    form_class = forms.NotificationContentUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("notificationcontent.change_notificationcontent",)
    }

    def get_success_url(self):
        return reverse('messageset:notificationcontent-list')


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

    def get_success_url(self):
        return reverse('messageset:sitemail-list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            sitemail = form.save(commit=False)
            sitemail.creator=request.user
            sitemail.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

class SiteMailContentUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = SiteMailContent
    form_class = forms.SiteMailContentUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("sitemailcontent.change_sitemailcontent",)
    }

    def get_success_url(self):
        return reverse('messageset:sitemailcontent-list')


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
        context['table_titles'] = [u'主题',  u'发件人', u'读取状态', u'收件时间'] + ['']
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
    filter_fields = ['title', 'content__contents', 'sender__name', 'status', 'creator__name', 'receiver__name']
    search_fields = ['title', 'content__contents', 'sender__name', 'status', 'creator__name', 'receiver__name']


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
        context['table_titles'] = ['Link'] + [u'主题', u'内容', u'发件人', u'读取状态', u'数据创建人', u'数据删除时间'] + ['']
        context['table_fields'] = ['link'] + ['title', 'content', 'sender', 'status', 'creator', 'deleted_at'] + ['id']
        return context


class TaskAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Task
    form_class = forms.TaskAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("task.add_task",)
    }

    def get_success_url(self):
        return reverse('messageset:task-list')


class TaskUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Task
    form_class = forms.TaskUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("task.change_task",)
    }

    def get_success_url(self):
        return reverse('messageset:task-list')


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
    filter_fields = ['name', 'percent', 'start_app', 'status', 'start_time', 'end_time', 'creator']
    search_fields = ['name', 'percent', 'start_app', 'status', 'start_time', 'end_time', 'creator']

