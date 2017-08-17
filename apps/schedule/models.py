from django.db import models
from django.utils.translation import ugettext_lazy as _


class OzbarginTask(models.Model):
    includes = models.CharField(_(u'includes'), max_length=255, null=False, blank=False)
    excludes = models.CharField(_(u'excludes'), max_length=255, null=False, blank=False)
    is_active = models.BooleanField(_(u'is_active'), default=True, blank=False, null=False)
    create_at = models.DateTimeField(_('Create at'), auto_now_add=True, null=True)
