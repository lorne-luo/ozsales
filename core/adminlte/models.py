from django.db import models
from django.utils.translation import ugettext_lazy as _

#
# class Country(models.Model):
#     name = models.CharField(_(u'name'), max_length=30, null=False, blank=False)
#     short_name = models.CharField(_(u'short_name'), max_length=30, null=True, blank=True)
#
#     class Meta:
#         verbose_name_plural = _('Country')
#         verbose_name = _('Country')
#
#     def __str__(self):
#         return '[%s]' % self.short_name
