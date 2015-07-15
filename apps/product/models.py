from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from apps.store.models import Page
from apps.common.models import Country
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    parent_category = models.ForeignKey('Category', default=None, blank=True, null=True, verbose_name=_('parent cate'))
    remarks = models.CharField(verbose_name=_('remarks'), max_length=500, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Category')
        verbose_name = _('Category')

    def __str__(self):
        return '[Cate]%s' % self.name


@python_2_unicode_compatible
class Brand(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    country = models.ForeignKey(Country, blank=True, null=True, verbose_name=_('country'))
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name=_('category'))

    class Meta:
        verbose_name_plural = _('Brand')
        verbose_name = _('Brand')

    def __str__(self):
        return '[B]%s' % self.name


@python_2_unicode_compatible
class Product(models.Model):
    name_cn = models.CharField(_(u'name'), max_length=254, null=False, blank=False)
    name_en = models.CharField(_(u'name'), max_length=254, null=True, blank=True)
    brand = models.ForeignKey(Brand, blank=True, null=True, verbose_name=_('brand'))
    category = models.ForeignKey(Category, blank=True, null=True, verbose_name=_('category'))
    bargain_price = models.DecimalField(_(u'bargain price'), max_digits=8, decimal_places=2, blank=True, null=True)
    page = models.ManyToManyField(Page, verbose_name=_('Page'), null=True, blank=True)


    class Meta:
        verbose_name_plural = _('Product')
        verbose_name = _('Product')

    def __str__(self):
        return '[P]%s' % self.name_cn



