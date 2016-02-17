from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Store(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    short_name = models.CharField(_(u'short name'), max_length=30, null=True, blank=True)
    address = models.CharField(_(u'address'), max_length=128, null=True, blank=True)
    domain = models.URLField(_(u'domain'), null=True, blank=True)
    search_url = models.URLField(_(u'Search URL'), null=True, blank=True)
    shipping_rate = models.CharField(_(u'Shipping Rate'), max_length=30, null=True, blank=True)

    class Meta:
        verbose_name_plural = _('Store')
        verbose_name = _('Store')

    def __str__(self):
        return '%s' % self.short_name

    class Config:

        # form_template_name = 'customer/customer_form.html'
        list_display_fields = [u'name', u'short_name', u'address', u'domain', u'Search URL', u'Shipping Rate']
        list_form_fields = [u'name', u'short_name', u'address', u'domain', u'Search URL', u'Shipping Rate']
        filter_fields = [u'name', u'short_name', u'address', u'domain']
        search_fields = [u'name', u'short_name', u'address', u'domain']

        @classmethod
        def filter_queryset(cls, request, queryset):
            queryset = Store.objects.all()
            return queryset


@python_2_unicode_compatible
class Page(models.Model):
    title = models.CharField(_(u'name'), max_length=254, null=False, blank=False)
    url = models.URLField(_(u'url'), null=False, blank=False)
    store = models.ForeignKey(Store, blank=True, null=True, verbose_name=_('Store'))
    price = models.DecimalField(_(u'price'), max_digits=8, decimal_places=2)
    original_price = models.DecimalField(_(u'original price'), max_digits=8, decimal_places=2)

    class Meta:
        verbose_name_plural = _('Page')
        verbose_name = _('Page')

    def __str__(self):
        return '%s' % self.title