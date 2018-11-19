# coding=utf-8
import logging
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.utils.translation import ugettext_lazy as _

log = logging.getLogger(__name__)


class Sms(models.Model):
    time = models.DateTimeField(_('DateTime'), auto_now_add=True, editable=False)
    app_name = models.CharField(_('App Name'), max_length=64, null=True, blank=True)
    send_to = models.CharField(_('Send To'), max_length=32, null=False, blank=False)
    content = models.CharField(_('Content'), max_length=255, null=True, blank=True)
    template_code = models.CharField(_('template code'), max_length=255, null=True, blank=True)
    biz_id = models.CharField(_('biz_id'), max_length=255, null=True, blank=True)
    remark = models.CharField(_('remark'), max_length=255, null=True, blank=True)
    success = models.BooleanField(_('Success'), default=False)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     # todo extract url from content
    #     super(Sms, self).save(force_insert, force_update, using, update_fields)

    def query_sms(self):
        if self.biz_id:
            # aliyun sms, china mobile
            from core.aliyun.sms.service import query_send_detail
            return query_send_detail(self.biz_id, self.send_to, 10, 1, self.time.strftime('%Y%m%d'))
        return None


@receiver(post_save, sender=Sms)
def sms_saved(sender, instance=None, created=False, **kwargs):
    if created and not instance.success:
        log.error('[SMS failed] %s' % instance.__dict__)
