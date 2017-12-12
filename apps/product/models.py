# coding=utf-8
import os
import uuid
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Sum, F, Q, Avg, Min, Max
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from pypinyin import Style
from stdimage import StdImageField
from taggit.managers import TaggableManager
from apps.member.models import Seller
from apps.store.models import Page
from django.utils.encoding import python_2_unicode_compatible

from core.auth_user.models import AuthUser
from core.libs.constants import COUNTRIES_CHOICES
from core.models.models import PinYinFieldModelMixin
from settings.settings import PRODUCT_PHOTO_FOLDER, MEDIA_URL


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    parent_category = models.ForeignKey('Category', default=None, blank=True, null=True, verbose_name=_('parent cate'))
    remarks = models.CharField(verbose_name=_('remarks'), max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Category')
        verbose_name = _('Category')

    def __str__(self):
        if self.parent_category:
            return '[%s]%s' % (self.parent_category.name, self.name)
        else:
            return self.name


@python_2_unicode_compatible
class Brand(models.Model):
    name_en = models.CharField(_('name_en'), max_length=128, blank=False, unique=True)
    name_cn = models.CharField(_('name_cn'), max_length=128, blank=True)
    short_name = models.CharField(_('Abbr'), max_length=128, blank=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name=_('category'))
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
    return os.path.join(instance.get_pic_path(), filename)


class ProductState(object):
    ON_SELL = 'ON_SELL'
    NOT_SELL = 'NOT_SELL'
    NO_STOCK = 'NO_STOCK'

    CHOICES = (
        (ON_SELL, ON_SELL),
        (NOT_SELL, NOT_SELL),
        (NO_STOCK, NO_STOCK)
    )


class ProductManager(models.Manager):
    def all_for_seller(self, obj):
        if isinstance(obj, Seller):
            seller_id = obj.id
        elif isinstance(obj, AuthUser) and obj.is_seller:
            seller_id = obj.profile.id
        else:
            return Product.objects.none()

        qs = super(ProductManager, self).get_queryset().filter(is_active=True).filter(
            Q(seller__isnull=True) | Q(seller_id=seller_id))
        return self.order_by_usage_for_seller(qs, seller_id)

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
class Product(PinYinFieldModelMixin, models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    code = models.CharField(_(u'code'), max_length=32, blank=True)
    name_en = models.CharField(_(u'name_en'), max_length=128, blank=True)
    name_cn = models.CharField(_(u'name_cn'), max_length=128, blank=True)
    brand_en = models.CharField(_(u'brand_en'), max_length=128, blank=True)
    brand_cn = models.CharField(_(u'brand_cn'), max_length=128, blank=True)
    country = models.CharField(_('country'), max_length=128, choices=COUNTRIES_CHOICES, default='AU', blank=True)
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    pic = StdImageField(upload_to=get_product_pic_path, blank=True, null=True, verbose_name=_('picture'),
                        variations={
                            'medium': {"width": 800, "height": 800},
                            'thumbnail': {"width": 400, "height": 400}
                        })
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name=_('brand'))
    spec = models.CharField(_(u'spec'), max_length=128, blank=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name=_('category'))
    weight = models.DecimalField(_(u'weight'), max_digits=8, decimal_places=2, blank=True, null=True)  # unit: KG
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
    ]
    objects = ProductManager()

    class Meta:
        verbose_name_plural = _('Product')
        verbose_name = _('Product')

    class Config:
        list_template_name = 'customer/adminlte-customer-list.html'

        # form_template_name = 'customer/customer_form.html'
        list_display_fields = ('name_en', 'name_cn', 'pic', 'brand', 'avg_sell_price')
        list_form_fields = ('name_en', 'name_cn', 'pic', 'brand', 'avg_sell_price')
        filter_fields = ('name_en', 'name_cn', 'brand__name_cn', 'brand__name_en')
        search_fields = ('name_en', 'name_cn', 'brand__name_cn', 'brand__name_en')

        @classmethod
        def filter_queryset(cls, request, queryset):
            queryset = Product.objects.all()
            return queryset

    def __str__(self):
        if self.brand and self.brand.name_en.lower() != 'none':
            return '%s %s' % (self.brand.name_en, self.name_cn)
        else:
            return self.name_cn

    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.set_uuid()

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

    def sell_price_text(self):
        return '%srmb' % self.safe_sell_price

    def stat(self):
        from apps.order.models import OrderProduct
        product_sales = OrderProduct.objects.filter(product_id=self.id).order_by('-id')
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

        self.save()


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
