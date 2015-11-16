import logging

from django import template

register = template.Library()
log = logging.getLogger(__name__)


@register.filter
def key(dict_, key_):
    """Returns key from given dict"""
    try:
        return dict_[key_]
    except KeyError as e:
        log.info(e)
