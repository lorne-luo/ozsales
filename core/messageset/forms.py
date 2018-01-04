# coding=utf-8
from core.django.forms import NoManytoManyHintModelForm
from models import Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task


class NotificationUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'receiver', 'status','read_time', 'creator']


class NotificationDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'receiver', 'status', 'read_time', 'creator']


class NotificationContentAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents']


class NotificationContentUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents', 'status', 'creator']


class NotificationContentDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['receivers', 'title', 'contents']


class SiteMailContentUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['receivers', 'title', 'contents']


class SiteMailReceiveAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender', 'status', 'creator', 'receiver', 'read_time']


class SiteMailReceiveUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender', 'status', 'creator', 'receiver', 'read_time']


class SiteMailReceiveDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender',  'status', 'creator', 'receiver', 'read_time']


class SiteMailSendAddForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['title', 'content', 'sender', 'status', 'creator']


class SiteMailSendUpdateForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['title', 'content', 'sender', 'status', 'creator']


class SiteMailSendDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['sender','title', 'content', 'status']


class TaskDetailForm(NoManytoManyHintModelForm):
    class Meta:
        model = Task
        fields = ['name', 'percent', 'start_app', 'status', 'end_time', 'creator']

