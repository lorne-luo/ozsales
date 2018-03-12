# coding=utf-8
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from braces.views import MultiplePermissionsRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from core.django.constants import ReadStatus
from core.django.views import CommonContextMixin
from .models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task
from . import forms


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
            notification_content = form.save(commit=False)
            notification_content.creator = request.user
            notification_content.save()
            form.save_m2m()
            notification_content.send()
            return redirect('messageset:notification-list')
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


# views for SiteMailContent
class SiteMailContentAddView(LoginRequiredMixin, CommonContextMixin, CreateView):
    model = SiteMailContent
    template_name = 'messageset/sitemail_form.html'

    def get_form_class(self):
        if self.request.user.is_superuser:
            return forms.SiteMailContentAddForm
        else:
            return forms.SiteMailContactAdminForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            sitemail = form.save(commit=False)
            sitemail.creator = request.user
            sitemail.save()
            form.save_m2m()
            sitemail.send()
            if request.user.is_superuser:
                return redirect('messageset:sitemail-list')
            else:
                messages.success(request, '发送成功.')
                return self.get(request, *args, **kwargs)
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

    def get_context_data(self, **kwargs):
        if self.object:
            mail_receive = SiteMailReceive.objects.filter(receiver=self.request.user, content=self.object)
            mail_receive.status = ReadStatus.READ
            mail_receive.save()
        return super(SiteMailContentDetailView, self).get_context_data(**kwargs)


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


# views for SiteMailSend
class SiteMailSendDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = SiteMailSend
    form_class = forms.SiteMailSendDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("sitemailsend.view_sitemailsend",)
    }


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
