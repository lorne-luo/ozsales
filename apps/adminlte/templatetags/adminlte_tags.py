#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from datetime import datetime
import django
# from django.db.models.fields.related import ManyRelatedManager
import django.db.models.fields.related as related
from django import template
from django.db.models import ImageField
from utils.converter import format_datetime


register = template.Library()


@register.filter(name='render_field_label')
def render_field_label(obj, field_name):
    if hasattr(obj, field_name):
        meta_fields = obj._meta.fields
        for mf in meta_fields:
            if mf.name == field_name:
                return mf.verbose_name

        many_to_many_fields = obj._meta.many_to_many
        for mf in many_to_many_fields:
            if mf.name == field_name:
                return mf.verbose_name

        return u'未知'
    else:
        return u''


@register.filter(name='render_field_value')
def render_field_value(obj, a):
    value = '-'
    if hasattr(obj, a):
        value = getattr(obj, a)
        if value is None:
            value = '-'
        else:
            if hasattr(value, 'field'):
                if isinstance(value.field, ImageField):
                    if value:
                        value = "<img style=\"height:90px\" src='%s' />" % value.url
                    else:
                        value = '<img style=\"height:90px\" src="/static/img/no_image.jpg" alt="没有图片" />'

            elif hasattr(obj, 'get_%s_display' % a):
                value = getattr(obj, 'get_%s_display' % a)()
            elif isinstance(value, datetime):
                value = format_datetime(value)
            elif isinstance(value, django.db.models.fields.related.RelatedField):
                pass
            elif hasattr(value, 'through'):
                objects = value.all()
                ret = ', '.join([unicode(o) for o in objects])
                return ret

    return value
