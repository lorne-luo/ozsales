# coding=utf-8
from core.libs.forms import ModelForm  # extend from django.forms.ModelForm
from django.utils.translation import ugettext_lazy as _
from models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task


class NotificationUpdateForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'receiver', 'status','read_time', 'creator']


class NotificationDetailForm(ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'receiver', 'status', 'read_time', 'creator']


class NotificationContentAddForm(ModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents']


class NotificationContentUpdateForm(ModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents', 'status', 'creator']


class NotificationContentDetailForm(ModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentAddForm(ModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['receivers', 'title', 'contents']


class SiteMailContentUpdateForm(ModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentDetailForm(ModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['receivers', 'title', 'contents']


class SiteMailReceiveAddForm(ModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender', 'status', 'creator', 'receiver', 'read_time']


class SiteMailReceiveUpdateForm(ModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender', 'status', 'creator', 'receiver', 'read_time']


class SiteMailReceiveDetailForm(ModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender',  'status', 'creator', 'receiver', 'read_time']


class SiteMailSendAddForm(ModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['title', 'content', 'sender', 'status', 'creator']


class SiteMailSendUpdateForm(ModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['title', 'content', 'sender', 'status', 'creator']


class SiteMailSendDetailForm(ModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['sender','title', 'content', 'status']


class TaskAddForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'percent', 'start_app', 'status', 'end_time', 'creator']


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'percent', 'start_app', 'status', 'end_time', 'creator']


class TaskDetailForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'percent', 'start_app', 'status', 'end_time', 'creator']

