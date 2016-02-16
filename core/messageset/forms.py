from django import forms
from models import AbstractMessageContent, AbstractSiteMail, Notification, NotificationContent, SiteMailContent, SiteMailReceive, SiteMailSend, Task


class NotificationAddForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'receive', 'status', 'read_time', 'creator']


class NotificationUpdateForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'receive', 'status','read_time', 'creator']


class NotificationDetailForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['title', 'content', 'receive', 'status', 'read_time', 'creator']


class NotificationContentAddForm(forms.ModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents', 'status', 'creator']


class NotificationContentUpdateForm(forms.ModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents', 'status', 'creator']


class NotificationContentDetailForm(forms.ModelForm):
    class Meta:
        model = NotificationContent
        fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentAddForm(forms.ModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['title', 'contents','receivers', 'status']


class SiteMailContentUpdateForm(forms.ModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['title', 'contents', 'status', 'creator']


class SiteMailContentDetailForm(forms.ModelForm):
    class Meta:
        model = SiteMailContent
        fields = ['title', 'contents', 'status', 'creator']


class SiteMailReceiveAddForm(forms.ModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender', 'status', 'creator', 'receive', 'read_time']


class SiteMailReceiveUpdateForm(forms.ModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender', 'status', 'creator', 'receive', 'read_time']


class SiteMailReceiveDetailForm(forms.ModelForm):
    class Meta:
        model = SiteMailReceive
        fields = ['title', 'content', 'sender',  'status', 'creator', 'receive', 'read_time']


class SiteMailSendAddForm(forms.ModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['title', 'content', 'sender', 'status', 'creator']


class SiteMailSendUpdateForm(forms.ModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['title', 'content', 'sender', 'status', 'creator']


class SiteMailSendDetailForm(forms.ModelForm):
    class Meta:
        model = SiteMailSend
        fields = ['title', 'content', 'sender', 'status', 'creator']


class TaskAddForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'percent', 'start_app', 'status', 'end_time', 'creator']


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'percent', 'start_app', 'status', 'end_time', 'creator']


class TaskDetailForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'percent', 'start_app', 'status', 'end_time', 'creator']

