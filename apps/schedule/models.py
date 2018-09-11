import dbsettings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.aliyun.sms.service import clean_mobile_number
from core.sms.telstra_api_v2 import send_au_sms


class DealSubscribe(models.Model):
    includes = models.CharField(_('includes'), max_length=255, null=False, blank=False)
    excludes = models.CharField(_('excludes'), max_length=255, null=True, blank=True)
    mobile = models.CharField(_('mobile'), max_length=15, null=True, blank=True)
    is_active = models.BooleanField(_('is_active'), default=True, blank=False, null=False)
    msg_count = models.IntegerField(_('message count'), default=0, blank=True, null=True)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True, null=True)

    def get_keyword_list(self):
        includes = self.includes.replace(',', ' ')
        return includes.split(' ')

    def get_exclude_list(self):
        excludes = self.excludes.replace(',', ' ')
        return excludes.split(' ')

    def send_msg(self, msg):
        mobile = clean_mobile_number(self.mobile)
        if not mobile:
            return

        if mobile.startswith('04'):
            # australia mobile
            send_au_sms(self.mobile, msg, 'DealSubscribe #%s' % self.pk)
        elif mobile.startswith('1'):
            # todo chinese mobile
            pass


# http://s.luotao.net/admin/settings/
class ForexRate(dbsettings.Group):
    AUDCNH = dbsettings.DecimalValue('AUD-RMB', default=5.2)
    USDCNH = dbsettings.DecimalValue('USD-RMB', default=6.5)
    EURCNH = dbsettings.DecimalValue('EUR-RMB', default=7.9)
    GBPCNH = dbsettings.DecimalValue('GBP-RMB', default=8.8)
    CADCNH = dbsettings.DecimalValue('CAD-RMB', default=5.23)
    NZDCNH = dbsettings.DecimalValue('NZD-RMB', default=4.7)
    JPYCNH = dbsettings.DecimalValue('JPY-RMB', default=0.058)


forex = ForexRate()
