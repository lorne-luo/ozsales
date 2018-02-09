from __future__ import absolute_import, unicode_literals
from django.db import models
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, MultiFieldPanel, InlinePanel, FieldRowPanel,
                                                PageChooserPanel, StreamFieldPanel, PageChooserPanel, TabbedInterface,
                                                ObjectList)

from apps.wagtail.home.blocks import BaseStreamBlock


class StaticPage(Page):
    template_name = models.CharField(max_length=255, blank=False, verbose_name='template name')

    def get_template(self, request, *args, **kwargs):
        if self.template_name:
            return self.template_name
        return super(StaticPage, self).get_template(request, *args, **kwargs)


class ContentPage(Page):
    content = StreamField(
        BaseStreamBlock(), verbose_name="Page content", blank=True
    )
    content_panels = Page.content_panels + [
        StreamFieldPanel('content'),
    ]


class HomePage(Page):
    pass
