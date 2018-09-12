from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager

from apps.tenant.models import Tenant
from core.aliyun.email.tasks import email_send_task
from core.auth_user.constant import ADMIN_GROUP
from core.payments.stripe.models import StripePaymentUserMixin
from core.sms.telstra_api_v2 import send_au_sms
from ..messageset.models import NotificationContent, SiteMailContent


class AuthUserManager(UserManager):
    def _create_user(self, password, is_staff, is_superuser, mobile=None, email=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not mobile and not email:
            raise ValueError('Mobile and email must give one')
        email = self.normalize_email(email)
        user = self.model(username=mobile or email, email=email, mobile=mobile, is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile=None, email=None, password=None, **extra_fields):
        return self._create_user(password, False, False, mobile, email, **extra_fields)

    def create_superuser(self, mobile, email, password, **extra_fields):
        return self._create_user(password, True, True, mobile=mobile, email=email, **extra_fields)

    def identify(self, mobile_or_email):
        if '@' in mobile_or_email:
            return super(AuthUserManager, self).get(email=mobile_or_email)
        else:
            return super(AuthUserManager, self).get(mobile=mobile_or_email)


class AuthUser(AbstractUser, StripePaymentUserMixin):
    WEBSITE = 'WEBSITE'
    WEIXIN = 'WEIXIN'
    USER_TYPE_CHOICES = (
        (WEBSITE, WEBSITE),
        (WEIXIN, WEIXIN),
    )
    mobile = models.CharField(_('mobile'), max_length=128, unique=True, blank=True)
    type = models.CharField(_('type'), max_length=32, choices=USER_TYPE_CHOICES, blank=True, default=WEBSITE)
    tenant_id = models.CharField(_('tenant_id'), max_length=128, blank=True)
    # if type is WEBSIT mobile field is mobile, if type is WEIXIN mobile field is openid

    objects = AuthUserManager()
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'mobile'

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    @cached_property
    def tenant(self):
        return Tenant.objects.filter(pk=self.tenant_id).first()

    @cached_property
    def profile(self):
        if getattr(self, 'seller', None):
            return getattr(self, 'seller')
        elif getattr(self, 'customer', None):
            return getattr(self, 'customer')
        return None

    @cached_property
    def is_seller(self):
        return getattr(self, 'seller', None) is not None

    @cached_property
    def is_customer(self):
        return getattr(self, 'customer', None) is not None

    def get_username(self):
        return self.mobile or self.email or self.username

    def in_group(self, group_names):
        if not isinstance(group_names, (list, tuple)):
            group_names = (group_names,)

        if self.is_superuser:
            return True
        user_groups = self.groups.values_list("name", flat=True)
        intersection = set(group_names).intersection(set(user_groups))
        return bool(intersection)

    @cached_property
    def subscriber(self):
        # for StripePaymentUserMixin, return correct djstripe subscriber
        return self

    @cached_property
    def is_admin(self):
        return self.is_superuser or self.in_group(ADMIN_GROUP)

    def email_user(self, subject, message, from_email=None, **kwargs):
        if self.email:
            email_send_task.apply_async(args=([self.email], subject, message))

    def send_au_sms(self, content, app_name=None):
        send_au_sms(self.mobile, content, app_name)

    def send_notification(self, title, content, sender=None):
        notification_content = NotificationContent(creator=sender, title=title, contents=content)
        notification_content.save()
        notification_content.receivers.add(self)
        notification_content.send()

    def send_sitemail(self, title, content, sender=None):
        sitemail_content = SiteMailContent(creator=sender, title=title, contents=content)
        sitemail_content.save()
        sitemail_content.receivers.add(self)
        sitemail_content.send()


class UserProfileMixin(object):
    @cached_property
    def profile(self):
        return self

    @cached_property
    def username(self):
        return self.auth_user.get_username()

    @cached_property
    def date_joined(self):
        return self.auth_user.date_joined

    @cached_property
    def is_admin(self):
        return self.auth_user.is_superuser or self.in_group(ADMIN_GROUP)

    @cached_property
    def is_active(self):
        return self.auth_user.is_active

    def in_group(self, group_names):
        return self.auth_user.in_group(group_names)
