from django import template
from ..models import Order

register = template.Library()


@register.simple_tag
def new_order_counter():
    return Order.objects.new().count()

@register.simple_tag
def shipping_order_counter():
    return Order.objects.shipping().count()

@register.simple_tag
def finished_order_counter():
    return Order.objects.finished().count()
