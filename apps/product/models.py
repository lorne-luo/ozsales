import os
import uuid
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Sum, F, Q
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from pypinyin import Style
from stdimage import StdImageField
from taggit.managers import TaggableManager

from apps.member.models import Seller
from apps.store.models import Page
from django.utils.encoding import python_2_unicode_compatible

from core.auth_user.models import AuthUser
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
    name_en = models.CharField(_('name_en'), max_length=128, null=False, blank=False, unique=True)
    name_cn = models.CharField(_('name_cn'), max_length=128, null=True, blank=True)
    short_name = models.CharField(_('Abbr'), max_length=128, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name=_('category'))
    remarks = models.CharField(verbose_name=_('remarks'), max_length=254, null=True, blank=True)

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
    if instance.spec1:
        filename = '%s_%s' % (filename, instance.spec1)
    if instance.spec2:
        filename = '%s_%s' % (filename, instance.spec2)
    if instance.spec3:
        filename = '%s_%s' % (filename, instance.spec3)
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

        qs = super(ProductManager, self).get_queryset().filter(Q(seller__isnull=True) | Q(seller_id=seller_id))
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
        return qs.annotate(use_counter=models.Count(models.Case(
            models.When(orderproduct__order__customer_id=customer_id, then=1),
            default=0,
            output_field=models.IntegerField()
        ))).order_by('-use_counter')


@python_2_unicode_compatible
class Product(PinYinFieldModelMixin, models.Model):
    seller = models.ForeignKey(Seller, blank=True, null=True)
    code = models.CharField(_(u'code'), max_length=32, null=True, blank=True)
    name_en = models.CharField(_(u'name_en'), max_length=128, null=False, blank=False)
    name_cn = models.CharField(_(u'name_cn'), max_length=128, null=False, blank=False)
    pinyin = models.TextField(_('pinyin'), max_length=512, blank=True)
    pic = StdImageField(upload_to=get_product_pic_path, blank=True, null=True, verbose_name=_('picture'),
                        variations={
                            'medium': {"width": 800, "height": 800},
                            'thumbnail': {"width": 400, "height": 400}
                        })
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name=_('brand'))
    spec1 = models.CharField(_(u'spec1'), max_length=128, null=True, blank=True)
    spec2 = models.CharField(_(u'spec2'), max_length=128, null=True, blank=True)
    spec3 = models.CharField(_(u'spec3'), max_length=128, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, verbose_name=_('category'))
    weight = models.DecimalField(_(u'weight'), max_digits=8, decimal_places=2, blank=True, null=True)  # unit: KG
    sold_count = models.IntegerField(_(u'Sold Count'), default=0, null=False, blank=False)
    full_price = models.DecimalField(_(u'full price'), max_digits=8, decimal_places=2, blank=True, null=True)
    sell_price = models.DecimalField(_(u'sell price'), max_digits=8, decimal_places=2, blank=True, null=True)

    normal_price = models.DecimalField(_(u'normal price'), max_digits=8, decimal_places=2, blank=True, null=True)
    bargain_price = models.DecimalField(_(u'bargain price'), max_digits=8, decimal_places=2, blank=True, null=True)
    safe_sell_price = models.DecimalField(_(u'safe sell price'), max_digits=8, decimal_places=2, blank=True, null=True)
    tb_url = models.URLField(_(u'TB URL'), null=True, blank=True)
    wd_url = models.URLField(_(u'WD URL'), null=True, blank=True)
    wx_url = models.URLField(_(u'WX URL'), null=True, blank=True)
    page = models.ManyToManyField(Page, verbose_name=_('page'), blank=True)
    uuid = models.CharField(max_length=36, unique=True, null=True, blank=True)

    summary = models.TextField(_(u'summary'), null=True, blank=True)
    description = models.TextField(_(u'description'), null=True, blank=True)
    state = models.CharField(_(u'state'), max_length=32, null=True, blank=True, default=ProductState.ON_SELL,
                             choices=ProductState.CHOICES)

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
        list_display_fields = ('name_en', 'name_cn', 'pic', 'brand', 'normal_price', 'bargain_price', 'safe_sell_price')
        list_form_fields = ('name_en', 'name_cn', 'pic', 'brand', 'normal_price', 'bargain_price', 'safe_sell_price')
        filter_fields = ('name_en', 'name_cn', 'brand__name_cn', 'brand__name_en')
        search_fields = ('name_en', 'name_cn', 'brand__name_cn', 'brand__name_en')

        @classmethod
        def filter_queryset(cls, request, queryset):
            queryset = Product.objects.all()
            return queryset

    def __str__(self):
        spec = ''
        if self.spec1:
            spec += ' ' + self.spec1
        if self.spec2:
            spec += ' ' + self.spec2
        if self.spec3:
            spec += ' ' + self.spec3

        if self.brand and self.brand.name_en.lower() != 'none':
            return '%s %s%s' % (self.brand.name_en, self.name_cn, spec)
        else:
            return '%s%s' % (self.name_cn, spec)

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
        spec = ''
        if self.spec1:
            spec += ' ' + self.spec1
        if self.spec2:
            spec += ' ' + self.spec2
        if self.spec3:
            spec += ' ' + self.spec3
        if self.brand and self.brand.name_en.lower() != 'none':
            return '%s %s%s' % (self.brand.name_cn, self.name_cn, spec)
        else:
            return '%s%s' % (self.name_cn, spec)

    get_name_cn.allow_tags = True
    get_name_cn.short_description = 'CN Name'

    def sell_price_text(self):
        return '%srmb' % self.safe_sell_price

    def stat_sold_count(self):
        from apps.order.models import OrderProduct
        data = OrderProduct.objects.filter(product_id=self.id).aggregate(sold_count=Sum(F('amount')))
        self.sold_count = data.get('sold_count') or 0
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
