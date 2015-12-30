import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from apps.store.models import Page
from django.utils.encoding import python_2_unicode_compatible
from settings.settings import PRODUCT_PHOTO_FOLDER, MEDIA_URL


@python_2_unicode_compatible
class Country(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    short_name = models.CharField(_(u'short_name'), max_length=30, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Country')
        verbose_name = _('Country')

    def __str__(self):
        return '[%s]' % self.short_name

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
    name_en = models.CharField(_(u'name_en'), max_length=128, null=False, blank=False)
    name_cn = models.CharField(_(u'name_cn'), max_length=128, null=True, blank=True)
    country = models.ForeignKey(Country, blank=True, null=True, verbose_name=_('country'))
    category = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_('category'))
    remarks = models.CharField(verbose_name=_('remarks'), max_length=254, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Brand')
        verbose_name = _('Brand')

    def __str__(self):
        return '%s' % self.name_en


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
    filename = filename.replace(' ', '-').replace('', '')
    filename = '%s%s%s.%s' % (PRODUCT_PHOTO_FOLDER, os.sep, filename, ext)
    return filename


@python_2_unicode_compatible
class Product(models.Model):
    name_en = models.CharField(_(u'name_en'), max_length=128, null=False, blank=False)
    name_cn = models.CharField(_(u'name_cn'), max_length=128, null=False, blank=False)
    pic = models.ImageField(upload_to=get_product_pic_path, blank=True, null=True, verbose_name=_('picture'))
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name=_('brand'))
    spec1 = models.CharField(_(u'spec1'), max_length=128, null=True, blank=True)
    spec2 = models.CharField(_(u'spec2'), max_length=128, null=True, blank=True)
    spec3 = models.CharField(_(u'spec3'), max_length=128, null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True, null=True, verbose_name=_('category'))
    normal_price = models.DecimalField(_(u'normal price'), max_digits=8, decimal_places=2, blank=True, null=True)
    bargain_price = models.DecimalField(_(u'bargain price'), max_digits=8, decimal_places=2, blank=True, null=True)
    safe_sell_price = models.DecimalField(_(u'safe sell price'), max_digits=8, decimal_places=2, blank=True, null=True)
    tb_url = models.URLField(_(u'TB URL'), null=True, blank=True)
    wd_url = models.URLField(_(u'WD URL'), null=True, blank=True)
    wx_url = models.URLField(_(u'WX URL'), null=True, blank=True)
    page = models.ManyToManyField(Page, verbose_name=_('page'), null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Product')
        verbose_name = _('Product')

    def __str__(self):
        spec = ''
        if self.spec1:
            spec += ' ' + self.spec1
        if self.spec2:
            spec += ' ' + self.spec2
        if self.spec3:
            spec += ' ' + self.spec3

        if self.brand:
            return '%s %s%s' % (self.brand.name_en, self.name_cn, spec)
        else:
            return '%s%s' % (self.name_cn, spec)

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
        return '%s %s %s' % (self.brand.name_en, self.name_cn, spec)

    get_name_cn.allow_tags = True
    get_name_cn.short_description = 'CN Name'

    def sell_price_text(self):
        return '%srmb' % self.safe_sell_price

