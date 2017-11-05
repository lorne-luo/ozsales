import logging

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from core.auth_user.constant import ADMIN_GROUP, MEMBER_GROUP, FREE_MEMBER_GROUP
from core.auth_user.models import AuthUser, UserProfileMixin
from core.sms.telstra_api import MessageSender

log = logging.getLogger(__name__)


@python_2_unicode_compatible
class Seller(UserProfileMixin, models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='seller',
                                     null=True, blank=True)
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    email = models.EmailField(_('email address'), blank=True)
    mobile = models.CharField(max_length=18, blank=True)
    expire_at = models.DateField(_('member expire at'), auto_now_add=False, editable=True, null=True, blank=True)
    start_at = models.DateField(_('member start at'), auto_now_add=False, editable=True, null=True, blank=True)

    def __str__(self):
        return '%s#%s' % (self.auth_user, self.name)

    def get_full_name(self):
        return self.name

    def check_expired(self):
        if self.in_group(FREE_MEMBER_GROUP) or self.auth_user.is_staff:
            # never expire
            return False
        elif self.in_group(MEMBER_GROUP):
            return timezone.now().date() > self.expire_at if self.expire_at else True
        else:
            log.info('seller[%s] have no group.' % self.auth_user.get_username())
            return True

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


class MembershipOrder(models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    start_at = models.DateField(_('membership start at'), auto_now_add=False, editable=True, null=True, blank=True)
    end_at = models.DateField(_('membership expire at'), auto_now_add=False, editable=True, null=True, blank=True)
    amount = models.DecimalField(_('membership payment'), max_digits=5, decimal_places=2, null=True)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True, null=True)
