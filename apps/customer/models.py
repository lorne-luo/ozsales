#coding:utf-8
import os

from django.db import models
from django.core.mail import send_mail
from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group, Permission
from django.db.models import Q
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.utils.http import urlquote
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.contrib.auth.hashers import is_password_usable, make_password
from settings.settings import BASE_DIR, ID_PHOTO_FOLDER, MEDIA_URL
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from apps.member.models import Seller


@python_2_unicode_compatible
class InterestTag(models.Model):
    name = models.CharField(_(u'name'), unique=True, max_length=30, null=False, blank=False)
    remarks = models.CharField(_('remarks'), max_length=254, null=True, blank=True)

    # tags = models.ManyToManyField(Customer, verbose_name=_('mobile number'), null=True, blank=True)

    class Meta:
        verbose_name_plural = _('InterestTags')
        verbose_name = _('InterestTag')

    def __str__(self):
        return '%s' % self.name


@python_2_unicode_compatible
class Customer(models.Model):
    seller = models.OneToOneField(Seller, blank=True, null=True, verbose_name=_('Member'))
    name = models.CharField(_('Name'), max_length=30, null=False, blank=False)
    email = models.EmailField(_('Email'), max_length=254, null=True, blank=True)
    mobile = models.CharField(_('Mobile'), max_length=15, null=True, blank=True,
                              validators=[validators.RegexValidator(r'^[\d-]+$', _('plz input validated mobile number'),
                                                                    'invalid')])
    order_count = models.PositiveIntegerField(_('Order Count'), null=True, blank=True, default=0)
    last_order_time = models.DateTimeField(_('Last order time'), auto_now_add=True, null=True)
    primary_address = models.ForeignKey('Address', blank=True, null=True, verbose_name=_('Primary Address'),
                                        related_name=_('primary_address'))
    tags = models.ManyToManyField(InterestTag, verbose_name=_('Tags'), blank=True)
    weixin_id = models.CharField(max_length=32, blank=True, null=True)  # 微信号

    # weixin user info
    # https://mp.weixin.qq.com/wiki/14/bb5031008f1494a59c6f71fa0f319c66.html
    # https://mp.weixin.qq.com/wiki/17/c0f37d5704f0b64713d5d2c37b468d75.html
    is_subscribe = models.BooleanField(default=False, blank=False, null=False)
    nickname = models.CharField(max_length=32, blank=True, null=True)
    openid = models.CharField(max_length=64, blank=True, null=True)
    sex = models.CharField(max_length=5, blank=True, null=True)
    province = models.CharField(max_length=32, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    language = models.CharField(max_length=64, null=True, blank=True)
    # 用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像）
    headimg_url = models.URLField(max_length=256, blank=True, null=True)
    privilege = models.CharField(max_length=256,blank=True, null=True)
    unionid = models.CharField(max_length=64, blank=True, null=True)
    subscribe_time = models.DateField(blank=True, null=True)
    remark = models.CharField(_('Remark'), max_length=128, null=True, blank=True)  # 公众号运营者对粉丝的备注
    groupid = models.CharField(max_length=256, null=True, blank=True)  # 用户所在的分组ID

    class Meta:
        verbose_name_plural = _('Customer')
        verbose_name = _('Customer')

    class Config:
        list_template_name = 'customer/adminlte-customer-list.html'
        # form_template_name = 'customer/customer_form.html'
        list_display_fields = ('name', 'mobile', 'order_count', 'last_order_time', 'primary_address', 'id')
        list_form_fields = ('name', 'email', 'mobile', 'primary_address', 'groups', 'tags')
        filter_fields = ('name', 'email', 'mobile')
        search_fields = ('name', 'email', 'mobile')

        @classmethod
        def filter_queryset(cls, request, queryset):
            queryset = Customer.objects.all()
            return queryset

    def __str__(self):
        return '%s' % self.name

    def get_link(self):
        url = reverse('admin:%s_%s_change' % ('customer', 'customer'), args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.name)

    def get_edit_link(self):
        url = reverse('customer:customer-update', args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.name)

    get_edit_link.short_description = 'Name'

    def get_detail_link(self):
        url = reverse('customer:customer-detail', args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.name)

    get_detail_link.short_description = 'Name'

    def add_order_link(self):
        # order_root = reverse('admin:app_list', kwargs={'app_label': 'order'})
        url = reverse('admin:%s_%s_add' % ('order', 'order'))
        url = '%s?customer_id=%s' % (url, self.id)
        return '<a href="%s">New Order</a>' % url

    add_order_link.allow_tags = True
    add_order_link.short_description = 'Add Order'

    def get_primary_address(self):
        if self.primary_address:
            addr = self.primary_address.get_address()
        elif self.address_set.count():
            addr = self.address_set.all()[0].get_address()
        else:
            addr = None

        return addr

    get_primary_address.allow_tags = False
    get_primary_address.short_description = 'Primary Addr'


@receiver(post_save, sender=Customer)
def customer_post_save(sender, instance=None, created=False, **kwargs):
    if not instance.primary_address:
        addr_set = instance.address_set.all()
        if addr_set.count():
            instance.primary_address = addr_set[0]
            instance.save(update_fields=['primary_address'])


def get_id_photo_front_path(instance, filename):
    ext = filename.split('.')[-1]
    count = instance.customer.address_set.count()
    filename = '%s_%s_front.%s' % (instance.customer.id, count + 1, ext)
    filename = os.path.join(ID_PHOTO_FOLDER, filename)
    return filename


def get_id_photo_back_path(instance, filename):
    ext = filename.split('.')[-1]
    count = instance.customer.address_set.count()
    filename = '%s_%s_back.%s' % (instance.customer.id, count + 1, ext)
    filename = os.path.join(ID_PHOTO_FOLDER, filename)
    return filename


@python_2_unicode_compatible
class Address(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    mobile = models.CharField(_('mobile number'), max_length=15, null=True, blank=True,
                              validators=[validators.RegexValidator(r'^[\d-]+$', _('plz input validated mobile number'),
                                                                    'invalid')])
    address = models.CharField(_('address'), max_length=100, null=False, blank=False)
    customer = models.ForeignKey(Customer, blank=False, null=False, verbose_name=_('customer'))
    id_number = models.CharField(_('ID number'), max_length=20, blank=True, null=True)
    id_photo_front = models.ImageField(_('ID Front'), upload_to=get_id_photo_front_path, blank=True, null=True)
    id_photo_back = models.ImageField(_('ID Back'), upload_to=get_id_photo_back_path, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Address')
        verbose_name = _('Address')

    def __str__(self):
        return self.get_text()

    def get_text(self):
        return u'%s,%s,%s' % (self.name, self.mobile, self.address)

    def get_customer_link(self):
        url = reverse('admin:customer_customer_change', args=[self.customer.id])
        return '<a href="%s">%s</a>' % (url, self.customer)

    get_customer_link.allow_tags = True
    get_customer_link.short_description = 'Customer'

    def id_photo_link(self):
        return self.id_photo_front_link() + self.id_photo_back_link()

    id_photo_link.allow_tags = True
    id_photo_link.short_description = 'ID_photo'

    def id_photo_front_link(self):
        if self.id_photo_front:
            file_path = str(self.id_photo_front)
            # base, file_path = file_path.split('/%s' % ID_PHOTO_FOLDER)
            # url = '/%s%s' % (ID_PHOTO_FOLDER, file_path)
            url = '%s%s' % (MEDIA_URL, file_path)
            return '<a target="_blank" href="%s"><img width="90px" src="%s"></a>' % (url, url)
        else:
            return ''

    id_photo_front_link.allow_tags = True
    id_photo_front_link.short_description = 'ID_photo_front'

    def id_photo_back_link(self):
        if self.id_photo_back:
            file_path = str(self.id_photo_back)
            # base, file_path = file_path.split('/%s' % ID_PHOTO_FOLDER)
            # url = '/%s%s' % (ID_PHOTO_FOLDER, file_path)
            url = '%s%s' % (MEDIA_URL, file_path)
            return '<a target="_blank" href="%s"><img width="90px" src="%s"></a>' % (url, url)
        else:
            return ''

    id_photo_back_link.allow_tags = True
    id_photo_back_link.short_description = 'ID_photo_back'

    def get_address(self):
        return '%s,%s,%s' % (self.name, self.mobile, self.address)
