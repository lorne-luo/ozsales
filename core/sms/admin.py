from django.forms import ModelForm
from django.contrib import admin
from .models import Sms


class SmsAdmin(admin.ModelAdmin):
    list_display = ('time', 'app_name', 'send_to', 'success')
    ordering = ['-id']

admin.site.register(Sms, SmsAdmin)
