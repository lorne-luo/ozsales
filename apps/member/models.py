import re
from datetime import timedelta
from django.db import models
from django.core.mail import send_mail
from dateutil.relativedelta import relativedelta
from django.core import validators
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import is_password_usable, make_password
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.http import urlquote
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.signals import user_logged_in, user_logged_out
from core.auth_user.models import AuthUser
from core.sms.telstra_api import MessageSender


@python_2_unicode_compatible
class Seller(models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='seller',
                                     null=True, blank=True)
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    email = models.EmailField(_('email address'), blank=True, null=False)
    mobile = models.CharField(max_length=18, null=True, blank=True)
    expire_at = models.DateField(_('member expire at'), auto_now_add=False, editable=True, null=True, blank=True)
    start_at = models.DateField(_('member start at'), auto_now_add=False, editable=True, null=True, blank=True)

    def __str__(self):
        return '[S#%s]%s' % (self.id, self.name)

    @property
    def username(self):
        return self.auth_user.username

    @property
    def date_joined(self):
        return self.auth_user.date_joined

    @property
    def is_active(self):
        return self.auth_user.is_active

    def get_full_name(self):
        return self.name

    def check_expiry(self):
        return timezone.now().date() > self.expire_at

    def enable(self, month):
        self.auth_user.is_active = True
        self.start_at = timezone.now().date()
        self.expire_at = self.start_at + relativedelta(months=month)
        self.auth_user.save(update_fields=['is_active'])
        self.save(update_fields=['start_at', 'expire_at'])

    def disable(self):
        self.auth_user.is_active = False
        self.auth_user.save(update_fields=['is_active'])

    def email_user(self, subject, message, from_email=None, **kwargs):
        if self.email:
            send_mail(subject, message, from_email, [self.email], **kwargs)

    def sms_user(self, content):
        if self.mobile:
            sender = MessageSender()
            sender.send_sms(self.mobile, content, app_name='SMS Seller')
