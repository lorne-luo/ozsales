import re
from django.db import models
from django.core.mail import send_mail
from django.core import validators
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import is_password_usable, make_password
from django.contrib.sessions.models import Session
from django.db.models import Q
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.http import urlquote
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.signals import user_logged_in, user_logged_out


@python_2_unicode_compatible
class Seller(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=30, unique=True, db_index=True, null=False, blank=False,
                                help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                            '@/./+/-/_ characters'),
                                validators=[
                                    validators.RegexValidator(re.compile(r'^[\w.@+-]+$'), _('Only letters, numbers and '
                                                                                            '@/./+/-/_ characters are allowed'),
                                                              'invalid')
                                ])
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    email = models.EmailField(_('email address'), max_length=254, null=True, blank=True)
    mobile = models.CharField(max_length=18, null=True, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('seller')
        verbose_name_plural = _('sellers')

    class Config:
        # list_template_name = 'customer/customer_list.html'
        # form_template_name = 'customer/customer_form.html'
        list_display_fields = ['username', 'name', 'email', 'mobile', 'is_active', 'date_joined']
        list_form_fields = ('username', 'name', 'email', 'mobile')
        filter_fields = ('username', 'name', 'email', 'mobile')
        search_fields = ('username', 'name', 'email', 'mobile')

        @classmethod
        def filter_queryset(cls, request, queryset):
            queryset = Seller.objects.all()
            return queryset

    def __str__(self):
        return '[S]%s' % self.name

    def get_full_name(self):
        return self.name.strip()

    def get_short_name(self):
        return self.name.strip()

    def clean(self):
        if not is_password_usable(self.password):
            self.password = make_password(self.password)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # Note: this is not called on bulk operations
        self.clean()
        super(Seller, self).save(force_insert, force_update, using, update_fields)

    def get_token(self):
        '''
         Get user's token for authentification via rest-api. Creates new if
         does not exist yet.
        '''
        token, _created = Token.objects.get_or_create(user=self)
        return token

    def renew_token(self):
        ''' Delete token and create a new one (since token is PK) '''
        token, created = Token.objects.get_or_create(user=self)

        if not created:
            token.delete()
            token, _created = Token.objects.get_or_create(user=self)

        return token

    @property
    def is_admin(self):
        return self.is_superuser or self.is_group('Admin')

    def is_group(self, group_name):
        return self.groups.filter(name=group_name).exists()

    def get_absolute_url(self):
        return "/profile/%s/" % urlquote(self.username)

    def email_user(self, subject, message, from_email=None):
        if self.email:
            send_mail(subject, message, from_email, [self.email])

    def logout_all(self):
        user_sessions = UserSession.objects.filter(user=self)
        for s in user_sessions:
            s.session.delete()
        user_sessions.delete()


class Profile(models.Model):
    user = models.OneToOneField(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=True, null=True)
    nickname = models.CharField(max_length=32, blank=True, null=True)
    wx_openid = models.CharField(max_length=64, blank=True, null=True)
    wx_id = models.CharField(max_length=32, blank=True, null=True)
    headimg_url = models.CharField(max_length=256, blank=True, null=True)
    mobile = models.CharField(max_length=18, blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    province = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    subscribe_time = models.DateField(blank=True, null=True)
    unionid = models.CharField(max_length=64, blank=True, null=True)
    remark = models.CharField(max_length=256, blank=True, null=True)
    group_id = models.IntegerField(blank=True, null=True)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.OneToOneField(Session, on_delete=models.CASCADE)


@receiver(user_logged_in)
def session_post_login(sender, request, user, **kwargs):
    request.session.save()
    UserSession.objects.get_or_create(
        session_id=request.session.session_key,
        defaults={
            'user': user
        }
    )


@receiver(user_logged_out)
def session_post_logout(sender, request, user, **kwargs):
    UserSession.objects.filter(session_id=request.session.session_key).delete()
