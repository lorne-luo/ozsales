import logging
import time

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djstripe.models import Plan
from rest_framework.authtoken.models import Token

from core.auth_user.constant import MEMBER_GROUP, PREMIUM_MEMBER_GROUP
from core.auth_user.models import AuthUser, UserProfileMixin
from core.django.constants import COUNTRIES_CHOICES
from core.payments.stripe.models import StripePaymentUserMixin
from core.payments.stripe.stripe_api import stripe

log = logging.getLogger(__name__)

MONTHLY_FREE_ORDER = 10
SELLER_MEMBER_PLAN_ID = 'Seller_Member_1'


@python_2_unicode_compatible
class Seller(UserProfileMixin, models.Model, StripePaymentUserMixin):
    country = models.CharField(_('country'), max_length=128, choices=COUNTRIES_CHOICES, default='AU', blank=True)
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='seller', null=True, blank=True)
    name = models.CharField(_('name'), max_length=30, null=True, blank=True)
    expire_at = models.DateField(_('member expire at'), auto_now_add=False, editable=True, null=True, blank=True)
    start_at = models.DateField(_('member start at'), auto_now_add=False, editable=True, null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

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

    def send_email(self, subject, message):
        self.auth_user.email_user(subject, message)

    def send_sms(self, content, app_name=None):
        self.auth_user.send_sms(content, app_name)

    def send_notification(self, title, content, sender=None):
        self.auth_user.send_notification(title, content, sender)

    def send_sitemail(self, title, content, sender=None):
        self.auth_user.send_sitemail(title, content, sender)

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

    def check_premium_member(self):
        if self.auth_user.is_superuser:
            return True  # always True
        elif self.in_group(PREMIUM_MEMBER_GROUP):
            return True
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

    def add_membership(self, charge, months=1):
        membership = MembershipOrder(seller=self)
        membership.start_at = timezone.now().date() if timezone.now().date() > self.expire_at else self.expire_at
        membership.end_at = membership.start_at + relativedelta(months=months)
        # membership.amount=charge.amount
        self.expire_at = membership.end_at
        membership.save()
        self.save(update_fields=['expire_at'])

    @staticmethod
    def create_seller(mobile, email, password, premium_account=False):
        user = AuthUser.objects.create_user(mobile=mobile, email=email, password=password)
        group = Group.objects.get(name=PREMIUM_MEMBER_GROUP) if premium_account else Group.objects.get(
            name=MEMBER_GROUP)
        user.groups.add(group)
        seller = Seller(auth_user=user, name=mobile or email)
        seller.save()


class MembershipOrder(models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    start_at = models.DateField(_('membership start at'), auto_now_add=False, editable=True, null=True, blank=True)
    end_at = models.DateField(_('membership expire at'), auto_now_add=False, editable=True, null=True, blank=True)
    amount = models.DecimalField(_('membership payment'), max_digits=5, decimal_places=2, null=True)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True, null=True)
