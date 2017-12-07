import logging

import time
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djstripe.models import Plan
from core.payments.stripe.stripe_api import stripe
from rest_framework.authtoken.models import Token

from core.auth_user.constant import ADMIN_GROUP, MEMBER_GROUP, FREE_MEMBER_GROUP
from core.auth_user.models import AuthUser, UserProfileMixin
from core.payments.stripe.models import UserProfileStripeMixin
from core.sms.telstra_api import MessageSender

log = logging.getLogger(__name__)

MONTHLY_FREE_ORDER = 10
SELLER_MEMBER_PLAN_ID = 'Seller_Member_1'


@python_2_unicode_compatible
class Seller(UserProfileMixin, models.Model, UserProfileStripeMixin):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='seller', null=True, blank=True)
    name = models.CharField(_('name'), max_length=30, null=True, blank=True)
    expire_at = models.DateField(_('member expire at'), auto_now_add=False, editable=True, null=True, blank=True)
    start_at = models.DateField(_('member start at'), auto_now_add=False, editable=True, null=True, blank=True)

    def __str__(self):
        if self.auth_user:
            return '%s#%s' % (self.name, self.auth_user.get_username())
        return '%s#%s' % (self.name, None)

    @property
    def email(self):
        return self.auth_user.email

    @property
    def mobile(self):
        return self.auth_user.mobile

    def set_email(self, email):
        self.auth_user.email = email
        self.auth_user.save(update_fields=['email'])

    def set_mobile(self, mobile):
        self.auth_user.mobile = mobile
        self.auth_user.save(update_fields=['mobile'])

    def get_name(self):
        return self.name or self.auth_user.get_username()

    @property
    def current_month_order_count(self):
        from apps.order.models import Order
        year = timezone.now().year
        month = timezone.now().month
        return Order.objects.filter(seller=self, create_time__year=year, create_time__month=month).count()

    def subscribe_seller_member(self):
        plan_id = SELLER_MEMBER_PLAN_ID
        if not self.stripe_customer.has_active_subscription(plan_id):
            plan = Plan.objects.filter(stripe_id=plan_id).first()
            next_month = timezone.now() + relativedelta(months=1)
            first_day = next_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            timestamp = int(time.mktime(first_day.timetuple()))
            self.stripe_customer.subscribe(plan, charge_immediately=False, trial_end=timestamp)
            # add invoice item for current month
            stripe.InvoiceItem.create(
                customer=self.stripe_customer.stripe_id,
                amount=int(plan.amount * 100),
                currency="aud",
                description="First month member plan fee",
            )

    def add_card(self, source, remove_old=False, set_default=True):
        card = super(Seller, self).add_card(source, remove_old=False, set_default=True)
        if card:
            self.subscribe_seller_member()
        return card

    def check_membership(self):
        if self.in_group(FREE_MEMBER_GROUP) or self.auth_user.is_staff:
            return True  # always True
        elif self.in_group(MEMBER_GROUP):
            if self.current_month_order_count <= MONTHLY_FREE_ORDER:
                return True  # in free range
            else:
                if self.can_charge():
                    if not self.stripe_customer.has_active_subscription(SELLER_MEMBER_PLAN_ID):
                        self.subscribe_seller_member()
                    return True  # paid seller
                else:
                    return False
        else:
            log.info('seller[%s] have no group.' % self.auth_user.get_username())
            return False

    def enable(self, month):
        self.auth_user.is_active = True
        self.start_at = timezone.now().date()
        self.expire_at = self.start_at + relativedelta(months=month)
        self.auth_user.save(update_fields=['is_active'])
        self.save(update_fields=['start_at', 'expire_at'])

    def disable(self):
        self.auth_user.is_active = False
        self.auth_user.save(update_fields=['is_active'])

    def send_email(self, subject, message, **kwargs):
        from_email = 'service@luotao.net'
        if self.email:
            send_mail(subject, message, from_email, [self.email], **kwargs)

    def send_sms(self, content):
        if self.mobile:
            if self.mobile.startswith('0'):
                # australia mobile
                sender = MessageSender()
                sender.send_sms(self.mobile, content, app_name='SMS Seller')
            elif self.mobile.startswith('1'):
                # china mobile
                pass

    def add_membership(self, charge, months=1):
        membership = MembershipOrder(seller=self)
        membership.start_at = timezone.now().date() if timezone.now().date() > self.expire_at else self.expire_at
        membership.end_at = membership.start_at + relativedelta(months=months)
        # membership.amount=charge.amount
        self.expire_at = membership.end_at
        membership.save()
        self.save(update_fields=['expire_at'])

    @staticmethod
    def create_seller(mobile, email, password, free_account=False):
        user = AuthUser.objects.create_user(mobile=mobile, email=email, password=password)
        group = Group.objects.get(name=FREE_MEMBER_GROUP) if free_account else Group.objects.get(name=MEMBER_GROUP)
        user.groups.add(group)
        seller = Seller(auth_user=user, name=mobile or email)
        seller.save()


class MembershipOrder(models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    start_at = models.DateField(_('membership start at'), auto_now_add=False, editable=True, null=True, blank=True)
    end_at = models.DateField(_('membership expire at'), auto_now_add=False, editable=True, null=True, blank=True)
    amount = models.DecimalField(_('membership payment'), max_digits=5, decimal_places=2, null=True)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True, null=True)
