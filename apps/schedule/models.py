from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core import validators
from core.sms.telstra_api import MessageSender


class DealSubscribe(models.Model):
    includes = models.CharField(_(u'includes'), max_length=255, null=False, blank=False)
    excludes = models.CharField(_(u'excludes'), max_length=255, null=True, blank=True)
    mobile = models.CharField(_(u'mobile'), max_length=15, null=True, blank=True)
    is_active = models.BooleanField(_(u'is_active'), default=True, blank=False, null=False)
    msg_count = models.IntegerField(_(u'message count'), blank=True, null=True, )
    create_at = models.DateTimeField(_(u'create at'), auto_now_add=True, null=True)

    def get_keyword_list(self):
        includes = self.includes.replace(',', ' ')
        return includes.split(' ')

    def get_exclude_list(self):
        excludes = self.excludes.replace(',', ' ')
        return excludes.split(' ')

    def send_msg(self, msg):
        sender = MessageSender()
        sender.send_sms(self.mobile, msg, 'DealSubscribe #%s' % self.id)
