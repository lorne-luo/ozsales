import re
from django.db import models
from django.core.mail import send_mail
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.contrib.auth.hashers import is_password_usable, make_password
from django.db.models import Q
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.utils.http import urlquote
from django.utils.encoding import python_2_unicode_compatible


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
        permissions = (

        )

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



