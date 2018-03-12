from django.db import models
from django.utils.translation import ugettext_lazy as _
from wagtail.contrib.settings.models import BaseSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel


@register_setting(icon='form')
class ContactUs(BaseSetting):
    name = models.CharField(_('name'), max_length=255, blank=True, help_text='contactor name')
    phone = models.CharField(_('phone'), max_length=32, blank=True, help_text='phone')
    email = models.EmailField(_('email'), max_length=255, blank=True, help_text='email')

    class Meta:
        verbose_name = 'contact us'
