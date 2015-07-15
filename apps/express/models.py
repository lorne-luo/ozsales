from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from ..order.models import Order


@python_2_unicode_compatible
class ExpressCompany(models.Model):
    name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
    website = models.URLField(_(u'website'), blank=True, null=True)
    search_url = models.URLField(_(u'search url'), blank=True, null=True)
    rate = models.DecimalField(_(u'rate'), max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '[EC]%s' % self.name


@python_2_unicode_compatible
class ExpressOrder(models.Model):
    carrier = models.ForeignKey(ExpressCompany, blank=False, null=False, verbose_name=_(u'carrier'))
    id_number = models.CharField(_(u'id number'), max_length=30, null=False, blank=False)
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_(u'order'))
    shipping_fee = models.DecimalField(_(u'shipping fee'), max_digits=8, decimal_places=2,
                                       blank=True, null=True)
    weight = models.DecimalField(_(u'weight'), max_digits=8, decimal_places=2, blank=True,
                                 null=True)
    remarks = models.TextField(verbose_name='remarks', max_length=500, null=True, blank=True)

    def __str__(self):
        return '[EX]%s' % self.name

    def get_track_url(self):
        if '%s' in self.carrier.search_url:
            return self.carrier.search_url % self.ticket_id
        else:
            return '%s?id=%s' % (self.carrier.search_url, self.ticket_id)
