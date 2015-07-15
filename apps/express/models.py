from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from ..order.models import Order


@python_2_unicode_compatible
class ExpressCarrier(models.Model):
    name_cn = models.CharField(_(u'name_cn'), max_length=50, null=False, blank=False)
    name_en = models.CharField(_(u'name_en'), max_length=50, null=True, blank=True)
    website = models.URLField(_(u'website'), blank=True, null=True)
    search_url = models.URLField(_(u'search url'), blank=True, null=True)
    rate = models.DecimalField(_(u'rate'), max_digits=6, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name_plural = _('Express Carrier')
        verbose_name = _('Express Carrier')

    def __str__(self):
        return '[EC]%s' % self.name_en


@python_2_unicode_compatible
class ExpressOrder(models.Model):
    carrier = models.ForeignKey(ExpressCarrier, blank=False, null=False, verbose_name=_(u'carrier'))
    express_id = models.CharField(_(u'express id'), max_length=30, null=False, blank=False)
    order = models.ForeignKey(Order, blank=False, null=False, verbose_name=_(u'order'))
    shipping_fee = models.DecimalField(_(u'shipping fee'), max_digits=8, decimal_places=2,
                                       blank=True, null=True)
    weight = models.DecimalField(_(u'weight'), max_digits=8, decimal_places=2, blank=True,
                                 null=True)
    remarks = models.TextField(verbose_name='remarks', max_length=500, null=True, blank=True)
    create_time = models.DateTimeField(_(u'create time'), auto_now_add=True, editable=True)

    class Meta:
        verbose_name_plural = _('Express Order')
        verbose_name = _('Express Order')

    def __str__(self):
        return '[EX]%s' % self.name

    def get_track_url(self):
        if '%s' in self.carrier.search_url:
            return self.carrier.search_url % self.ticket_id
        else:
            return '%s?id=%s' % (self.carrier.search_url, self.ticket_id)

    def tracking_link(self):
        return '<a target="_blank" href="%s">%s</a>' % (self.get_track_url(), self.id_number)

    tracking_link.allow_tags = True
    tracking_link.short_description = 'ID'