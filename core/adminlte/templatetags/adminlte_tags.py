#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from datetime import datetime
import django
import django.db.models.fields.related as related
from django import template
from django.db.models import ImageField
from utils.converter import format_datetime

register = template.Library()


def get_attr(obj, attr_name):
    """
    当attr_name中包含'.'时，获取属性值
    :param obj:
    :param attr_name:
    :return:
    """
    if '.' in attr_name:
        lst_attr = [obj]
        lst_attr.extend(attr_name.split('.'))
        return reduce(getattr, lst_attr)
    else:
        return getattr(obj, attr_name)


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
    if hasattr(obj, a) or '.' in a:
        value = get_attr(obj, a)
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


@register.filter
def startswith(value, arg):
    """Usage, {% if value|starts_with:"arg" %}"""
    return value.startswith(arg)


@register.filter
def endswith(value, arg):
    """Usage, {% if value|endswith:"arg" %}"""
    return value.endswith(arg)


@register.filter
def split(value, arg):
    """Usage, {% if value|split:"," %}"""
    return value.split(arg)
