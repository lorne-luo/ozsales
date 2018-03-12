from django import template
from ..models import Customer

register = template.Library()


@register.simple_tag
def customer_counter():
    return Customer.objects.count()


