# coding=utf-8
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)


class Sms(models.Model):
    time = models.DateTimeField(_(u'DateTime'), auto_now_add=True, editable=False)
    app_name = models.CharField(_(u'App Name'), max_length=64, null=True, blank=True)
    send_to = models.CharField(_(u'Send To'), max_length=32, null=False, blank=False)
    content = models.CharField(_(u'Content'), max_length=255, null=True, blank=True)
    url = models.URLField(_(u'Url'), max_length=255, null=True, blank=True)
    success = models.BooleanField(_(u'Success'), default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # todo extract url from content
        super(Sms, self).save()
