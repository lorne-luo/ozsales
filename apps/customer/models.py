# coding:utf-8
import os

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Manager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from pypinyin import Style
from stdimage import StdImageField

from core.aliyun.email.tasks import email_send_task
from core.auth_user.models import AuthUser, UserProfileMixin
from core.django.models import PinYinFieldModelMixin, ResizeUploadedImageModelMixin, TenantModelMixin

from apps.member.models import Seller
from apps.product.models import Product
from core.django.storage import OverwriteStorage


class InterestTag(models.Model):
    name = models.CharField(_('name'), unique=True, max_length=30, null=False, blank=False)
    remarks = models.CharField(_('remarks'), max_length=254, null=True, blank=True)

    # tags = models.ManyToManyField(Customer, verbose_name=_('mobile number'), null=True, blank=True)

    class Meta:
        verbose_name_plural = _('InterestTags')
        verbose_name = _('InterestTag')

    def __str__(self):
        return '%s' % self.name


class Customer(PinYinFieldModelMixin, UserProfileMixin, TenantModelMixin, models.Model):
    auth_user = models.OneToOneField(AuthUser, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    seller = models.ForeignKey(Seller, blank=True, null=True, verbose_name=_('seller'))
    name = models.CharField(_('姓名'), max_length=30, null=False, blank=False)
    remark = models.CharField(_('备注'), max_length=255, blank=True)
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    email = models.EmailField(_('Email'), max_length=255, blank=True)
    mobile = models.CharField(_('手机'), max_length=15, blank=True)
    order_count = models.PositiveIntegerField(_('订单数'), blank=True, default=0)
    last_order_time = models.DateTimeField(_('Last order time'), auto_now_add=True, null=True)
    primary_address = models.ForeignKey('Address', blank=True, null=True, verbose_name=_('默认地址'),
                                        related_name='primary_address')
    tags = models.ManyToManyField(InterestTag, verbose_name=_('Tags'), blank=True)

    pinyin_fields_conf = [
        ('name', Style.NORMAL, False),
        ('name', Style.FIRST_LETTER, False),
        ('remark', Style.NORMAL, False),
        ('remark', Style.FIRST_LETTER, False),
    ]

    class Meta:
        verbose_name_plural = _('Customer')
        verbose_name = _('Customer')

    def __str__(self):
        return '%s' % self.name

    @property
    def name_and_remarks(self):
        if self.remark:
            return '%s (%s)' % (self.name, self.remark)
        return '%s' % self.name

    @property
    def profile(self):
        return self

    @property
    def total_spend(self):
        return sum([x.sell_price_rmb for x in self.order_set.all()])

    @property
    def total_spend_year(self):
        """total spend in recent one year"""
        year_before = timezone.now() - relativedelta(years=1)
        return sum([x.sell_price_rmb for x in self.order_set.all().filter(finish_time__gt=year_before)])

    def get_link(self):
        url = reverse('admin:%s_%s_change' % ('customer', 'customer'), args=[self.pk])
        return '<a href="%s">%s</a>' % (url, self.name)

    def get_edit_link(self):
        url = reverse('customer:customer-update', args=[self.pk])
        return '<a href="%s">%s</a>' % (url, self.name)

    get_edit_link.short_description = 'Name'

    def get_detail_link(self):
        url = reverse('customer:customer-detail', args=[self.pk])
        return '<a href="%s">%s</a>' % (url, self.name)

    get_detail_link.short_description = 'Name'

    def add_order_link(self):
        # order_root = reverse('admin:app_list', kwargs={'app_label': 'order'})
        url = reverse('admin:%s_%s_add' % ('order', 'order'))
        url = '%s?customer_id=%s' % (url, self.pk)
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

    def send_email(self, subject, message):
        if self.email:
            email_send_task.apply_async(args=([self.email], subject, message))


@receiver(post_save, sender=Customer)
def customer_post_save(sender, instance=None, created=False, **kwargs):
    if not instance.primary_address_id:
        addr_set = instance.address_set.all()
        if addr_set.count():
            instance.primary_address = addr_set[0]
            instance.save(update_fields=['primary_address'])


def get_id_photo_front_path(instance, filename):
    ext = filename.split('.')[-1]
    count = instance.customer.address_set.count()
    filename = '%s_%s_front.%s' % (instance.customer.pk, count + 1, ext)
    file_path = os.path.join(settings.ID_PHOTO_FOLDER, filename)

    from apps.schedule.tasks import guetzli_compress_image
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    guetzli_compress_image.apply_async(args=[full_path], countdown=10)
    return file_path


def get_id_photo_back_path(instance, filename):
    ext = filename.split('.')[-1]
    count = instance.customer.address_set.count()
    filename = '%s_%s_back.%s' % (instance.customer.pk, count + 1, ext)
    file_path = os.path.join(settings.ID_PHOTO_FOLDER, filename)

    from apps.schedule.tasks import guetzli_compress_image
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    guetzli_compress_image.apply_async(args=[full_path], countdown=230)
    return file_path


class AddressManager(Manager):
    def belong_to(self, obj):
        if isinstance(obj, Customer):
            customer_id = obj.pk
            return super(AddressManager, self).get_queryset().filter(customer_id=customer_id)
        elif isinstance(obj, AuthUser) and obj.is_customer:
            customer_id = obj.profile.pk
            return super(AddressManager, self).get_queryset().filter(customer_id=customer_id)
        else:
            raise PermissionDenied


class Address(ResizeUploadedImageModelMixin, PinYinFieldModelMixin, TenantModelMixin, models.Model):
    name = models.CharField(_('name'), max_length=30, null=False, blank=False)
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    mobile = models.CharField(_('mobile number'), max_length=15, null=True, blank=True)
    address = models.CharField(_('address'), max_length=100, null=False, blank=False)
    customer = models.ForeignKey(Customer, blank=False, null=False, verbose_name=_('customer'))
    id_number = models.CharField(_('ID number'), max_length=20, blank=True, null=True)
    id_photo_front = StdImageField(_('ID Front'), upload_to=get_id_photo_front_path, blank=True, null=True,
                                   storage=OverwriteStorage(),
                                   variations={
                                       'thumbnail': (150, 150, False)
                                   })
    id_photo_back = StdImageField(_('ID Back'), upload_to=get_id_photo_back_path, blank=True, null=True,
                                  storage=OverwriteStorage(),
                                  variations={
                                      'thumbnail': (150, 150, False)
                                  })

    objects = AddressManager()
    pinyin_fields_conf = [
        ('name', Style.NORMAL, False),
        ('name', Style.FIRST_LETTER, False),
        ('address', Style.NORMAL, False),
        ('address', Style.FIRST_LETTER, False),
    ]

    class Meta:
        verbose_name_plural = _('Address')
        verbose_name = _('Address')

    def __str__(self):
        return self.get_text()

    def get_text(self):
        text = self.address
        if self.mobile:
            text = '%s,%s' % (self.mobile, text)
        if self.name:
            text = '%s,%s' % (self.name, text)
        return text

    def get_customer_link(self):
        url = reverse('admin:customer_customer_change', args=[self.customer.pk])
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
            # base, file_path = file_path.split('/%s' % settings.ID_PHOTO_FOLDER)
            # url = '/%s%s' % (settings.ID_PHOTO_FOLDER, file_path)
            url = '%s%s' % (settings.MEDIA_URL, file_path)
            return '<a target="_blank" href="%s"><img width="90px" src="%s"></a>' % (url, url)
        else:
            return ''

    id_photo_front_link.allow_tags = True
    id_photo_front_link.short_description = 'ID_photo_front'

    def id_photo_back_link(self):
        if self.id_photo_back:
            file_path = str(self.id_photo_back)
            # base, file_path = file_path.split('/%s' % settings.ID_PHOTO_FOLDER)
            # url = '/%s%s' % (settings.ID_PHOTO_FOLDER, file_path)
            url = '%s%s' % (settings.MEDIA_URL, file_path)
            return '<a target="_blank" href="%s"><img width="90px" src="%s"></a>' % (url, url)
        else:
            return ''

    id_photo_back_link.allow_tags = True
    id_photo_back_link.short_description = 'ID_photo_back'

    def get_address(self):
        return '%s,%s,%s' % (self.name, self.mobile, self.address)

    def save(self, *args, **kwargs):
        # resize images when first uploaded
        self.resize_image('id_photo_front')
        self.resize_image('id_photo_back')
        if self.id_number and 'x' in self.id_number:
            self.id_number = self.id_number.upper()

        self.link_id_photo()
        super(Address, self).save(*args, **kwargs)

    def link_id_photo(self):
        if self.id_number:
            existed = None
            if not self.id_photo_front:
                existed = Address.objects.filter(id_number=self.id_number, id_photo_front__isnull=False).first()
                if existed:
                    self.id_photo_front = existed.id_photo_front
            if not self.id_photo_back:
                if existed and existed.id_photo_back:
                    self.id_photo_back = existed.id_photo_back
                else:
                    existed = Address.objects.filter(id_number=self.id_number, id_photo_back__isnull=False).first()
                    if existed:
                        self.id_photo_back = existed.id_photo_back

# @receiver(post_delete, sender=CartProduct)
# def cart_product_deleted(sender, **kwargs):
#     cart_product = kwargs['instance']
#     cart_product.cart.update_price()
#
#
# @receiver(post_save, sender=CartProduct)
# def cart_product_post_save(sender, instance=None, created=False, update_fields=None, **kwargs):
#     if instance.cart:
#         instance.cart.update_price()
