# coding=utf-8
import logging
import os
import uuid
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Sum, F, Avg, Min, Max
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from pypinyin import Style
from stdimage import StdImageField
from taggit.managers import TaggableManager

from core.auth_user.models import AuthUser
from core.django.constants import COUNTRIES_CHOICES
from core.django.models import PinYinFieldModelMixin, ResizeUploadedImageModelMixin
from config.settings import PRODUCT_PHOTO_FOLDER, MEDIA_URL, MEDIA_ROOT

from apps.member.models import Seller
from apps.store.models import Page

log = logging.getLogger(__name__)


@python_2_unicode_compatible
class Brand(models.Model):
    name_en = models.CharField(_('name_en'), max_length=128, blank=False, unique=True)
    name_cn = models.CharField(_('name_cn'), max_length=128, blank=True)
    short_name = models.CharField(_('Abbr'), max_length=128, blank=True)
    remarks = models.CharField(verbose_name=_('remarks'), max_length=254, blank=True)

    class Meta:
        verbose_name_plural = _('Brand')
        verbose_name = _('Brand')

    def __str__(self):
        if self.name_en.lower() == 'none':
            return ''
        else:
            return self.name_en


def get_product_pic_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = instance.brand.name_en + '_' if instance.brand.name_en else ''
    filename = '%s%s' % (filename, instance.name_en)
    filename = filename.replace(' ', '-')
    filename = '%s.%s' % (filename, ext)
    file_path = os.path.join(PRODUCT_PHOTO_FOLDER, filename)

    from apps.schedule.tasks import guetzli_compress_image
    full_path = os.path.join(MEDIA_ROOT, file_path)
    guetzli_compress_image.apply_async(args=[full_path], countdown=10)
    return file_path


class ProductManager(models.Manager):
    DEFAULT_CACHE_KEY = 'QUERYSET_CACHE_DEFAULT_PRODUCT'

    def clean_cache(self):
        log.info('[QUERYSET_CACHE] clean carriers.')
        cache.delete(self.DEFAULT_CACHE_KEY)

    def default(self):
        default_product = cache.get_or_set(
            self.DEFAULT_CACHE_KEY,
            super(ProductManager, self).get_queryset().filter(is_active=True, seller__isnull=True),
            24 * 60 * 60)
        return default_product

    def all_for_seller(self, obj):
        if isinstance(obj, Seller):
            seller_id = obj.id
        elif isinstance(obj, AuthUser) and obj.is_seller:
            seller_id = obj.profile.id
        else:
            return Product.objects.none()

        default_product = self.default()
        qs = default_product | super(ProductManager, self).get_queryset().filter(is_active=True, seller_id=seller_id)
        return qs

    def order_by_usage_for_seller(self, qs, seller_id):
        return qs.annotate(use_counter=models.Count(models.Case(
            models.When(orderproduct__order__seller_id=seller_id, then=1),
            default=0,
            output_field=models.IntegerField()
        ))).order_by('-use_counter')

    def all_for_customer(self, obj):
        from apps.customer.models import Customer
        if isinstance(obj, Customer):
            customer_id = obj.id
        elif isinstance(obj, AuthUser) and obj.is_customer:
            customer_id = obj.profile.id
        else:
            return Product.objects.none()

        qs = super(ProductManager, self).get_queryset()
        return self.order_by_usage_for_customer(qs, customer_id)

    def order_by_usage_for_customer(self, qs, customer_id):
        return qs.filter(is_active=True).annotate(use_counter=models.Count(models.Case(
            models.When(orderproduct__order__customer_id=customer_id, then=1),
            default=0,
            output_field=models.IntegerField()
        ))).order_by('-use_counter')


@python_2_unicode_compatible
class Product(ResizeUploadedImageModelMixin, PinYinFieldModelMixin, models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    code = models.CharField(_(u'code'), max_length=32, blank=True)
    name_en = models.CharField(_(u'name_en'), max_length=128, blank=True)
    name_cn = models.CharField(_(u'name_cn'), max_length=128, blank=True)
    brand_en = models.CharField(_(u'brand_en'), max_length=128, blank=True)
    brand_cn = models.CharField(_(u'brand_cn'), max_length=128, blank=True)
    alias = models.CharField(_(u'alias'), max_length=255, blank=True)
    country = models.CharField(_('country'), max_length=128, choices=COUNTRIES_CHOICES, default='AU', blank=True)
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    pic = StdImageField(upload_to=get_product_pic_path, blank=True, null=True, verbose_name=_('picture'),
                        variations={
                            'medium': (800, 800, True),
                            'thumbnail': (400, 400, True)
                        })
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name=_('brand'))
    spec = models.CharField(_(u'spec'), max_length=128, blank=True)
    # deliver weight unit: KG
    weight = models.DecimalField(_(u'weight'), max_digits=8, decimal_places=2, blank=True, null=True)
    sold_count = models.IntegerField(_(u'Sold Count'), default=0, null=False, blank=False)

    last_sell_price = models.DecimalField(_(u'last sell price'), max_digits=8, decimal_places=2, blank=True, null=True)
    avg_sell_price = models.DecimalField(_(u'avg sell price'), max_digits=8, decimal_places=2, blank=True, null=True)
    min_sell_price = models.DecimalField(_(u'min sell price'), max_digits=8, decimal_places=2, blank=True, null=True)
    max_sell_price = models.DecimalField(_(u'max sell price'), max_digits=8, decimal_places=2, blank=True, null=True)
    avg_cost = models.DecimalField(_(u'avg cost'), max_digits=8, decimal_places=2, blank=True, null=True)
    min_cost = models.DecimalField(_(u'min cost'), max_digits=8, decimal_places=2, blank=True, null=True)
    max_cost = models.DecimalField(_(u'max cost'), max_digits=8, decimal_places=2, blank=True, null=True)

    safe_sell_price = models.DecimalField(_(u'safe sell price'), max_digits=8, decimal_places=2, blank=True, null=True)
    tb_url = models.URLField(_(u'TB URL'), null=True, blank=True)
    wd_url = models.URLField(_(u'WD URL'), null=True, blank=True)
    wx_url = models.URLField(_(u'WX URL'), null=True, blank=True)
    page = models.ManyToManyField(Page, verbose_name=_('page'), blank=True)
    uuid = models.CharField(max_length=36, unique=True, null=True, blank=True)

    summary = models.TextField(_(u'summary'), null=True, blank=True)
    description = models.TextField(_(u'description'), null=True, blank=True)
    is_active = models.BooleanField(_(u'is active'), default=True, null=False, blank=False)

    tags = TaggableManager()
    pinyin_fields_conf = [
        ('name_cn', Style.NORMAL, False),
        ('name_cn', Style.FIRST_LETTER, False),
        ('brand.name_cn', Style.NORMAL, False),
        ('brand.name_cn', Style.FIRST_LETTER, False),
        ('alias', Style.NORMAL, False),
        ('alias', Style.FIRST_LETTER, False),
    ]
    objects = ProductManager()

    class Meta:
        verbose_name_plural = _('Product')
        verbose_name = _('Product')

    def __str__(self):
        if self.brand and self.brand.name_en.lower() != 'none':
            return '%s %s' % (self.brand.name_en, self.name_cn)
        else:
            return self.name_cn

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.set_uuid()
        field_names = ['seller', 'name_en', 'name_cn', 'brand_id', 'brand_en', 'brand_cn']
        for field_name in set(field_names):
            current_value = self.get_attr_by_str(field_name)
            self._original_fields_value.update({field_name: current_value})

    def set_uuid(self):
        if not self.uuid:
            uuid_str = uuid.uuid4().hex
            while (Product.objects.filter(uuid=uuid_str).exists()):
                uuid_str = uuid.uuid4().hex

            self.uuid = uuid_str

    def get_pic_path(self):
        if not self.uuid:
            self.set_uuid()
        return os.path.join(PRODUCT_PHOTO_FOLDER, self.uuid)

    def get_edit_link(self):
        url = reverse('product:product-update-view', args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.name_cn)

    get_edit_link.short_description = 'Name'

    def get_detail_link(self):
        url = reverse('product:product-detail-view', args=[self.id])
        return u'<a href="%s">%s</a>' % (url, self.name_cn)

    get_detail_link.short_description = 'Name'

    def get_pic_link(self):
        if self.pic:
            file_path = str(self.pic)
            # base, file_path = file_path.split('/%s' % ID_PHOTO_FOLDER)
            # url = '/%s%s' % (ID_PHOTO_FOLDER, file_path)
            url = '%s%s' % (MEDIA_URL, file_path)
            return '<a target="_blank" href="%s"><img height="60px" src="%s"></a>' % (url, url)
        else:
            return ''

    get_pic_link.allow_tags = True
    get_pic_link.short_description = 'Pic'

    def get_name_cn(self):
        if self.brand and self.brand.name_en.lower() != 'none':
            return '%s %s' % (self.brand.name_cn, self.name_cn)
        else:
            return self.name_cn

    get_name_cn.allow_tags = True
    get_name_cn.short_description = 'CN Name'

    def stat(self):
        from apps.order.models import OrderProduct
        product_sales = OrderProduct.objects.filter(product_id=self.id).exclude(
            sell_price_rmb=0).exclude(cost_price_aud=0).order_by('-id')
        if product_sales.count():
            data = product_sales.aggregate(sold_count=Sum(F('amount')),
                                           avg_sell_price=Avg(F('sell_price_rmb')),
                                           min_sell_price=Min(F('sell_price_rmb')),
                                           max_sell_price=Max(F('sell_price_rmb')),
                                           avg_cost=Avg(F('cost_price_aud')),
                                           min_cost=Min(F('cost_price_aud')),
                                           max_cost=Max(F('cost_price_aud')))
            self.last_sell_price = product_sales.first().sell_price_rmb
            self.sold_count = data.get('sold_count') or 0
            self.avg_sell_price = data.get('avg_sell_price') or None
            self.min_sell_price = data.get('min_sell_price') or None
            self.max_sell_price = data.get('max_sell_price') or None
            self.avg_cost = data.get('avg_cost') or None
            self.min_cost = data.get('min_cost') or None
            self.max_cost = data.get('max_cost') or None
        else:
            self.last_sell_price = None
            self.sold_count = 0
            self.avg_sell_price = None
            self.min_sell_price = None
            self.max_sell_price = None
            self.avg_cost = None
            self.min_cost = None
            self.max_cost = None

        self.save(update_cache=False)

    def assign_brand(self):
        if self.brand:
            self.brand_cn = self.brand.name_cn if not self.brand_cn else self.brand_cn
            self.brand_en = self.brand.name_en if not self.brand_en else self.brand_en
        else:
            if self.brand_en:
                self.brand = Brand.objects.filter(name_en=self.brand_en).first()
            elif self.brand_cn:
                self.brand = Brand.objects.filter(name_cn=self.brand_cn).first()

    def save(self, *args, **kwargs):
        self.assign_brand()
        self.resize_image('pic')  # resize images when first uploaded

        update_cache = kwargs.pop('update_cache', True)  # default to update cache
        super(Product, self).save(*args, **kwargs)
        if update_cache:
            Product.objects.clean_cache()


@receiver(post_delete, sender=Product)
def product_deleted(sender, **kwargs):
    instance = kwargs['instance']
    if instance.seller is None:  # default carrier, clean cache
        Product.objects.clean_cache()


# ========================= product sub model ==================================

class DefaultProductManager(models.Manager):
    def get_queryset(self):
        return super(DefaultProductManager, self).get_queryset().filter(seller__isnull=True)


class DefaultProduct(Product):
    objects = DefaultProductManager()

    class Meta:
        proxy = True


class CustomProductManager(models.Manager):
    def get_queryset(self):
        return super(CustomProductManager, self).get_queryset().filter(seller__isnull=False)

    def belong_to(self, obj):
        if isinstance(obj, Seller):
            seller_id = obj.id
        elif isinstance(obj, AuthUser) and obj.is_seller:
            seller_id = obj.profile.id
        else:
            return Product.objects.none()

        return super(CustomProductManager, self).get_queryset().filter(seller_id=seller_id)


class CustomProduct(Product):
    objects = CustomProductManager()

    class Meta:
        proxy = True
