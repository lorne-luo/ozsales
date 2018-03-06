from django import template
from ..models import ExpressOrder

register = template.Library()


@register.simple_tag
def parcel_counter():
    return ExpressOrder.objects.count()

