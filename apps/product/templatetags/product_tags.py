from django import template
from ..models import Product

register = template.Library()


@register.simple_tag
def product_counter():
    return Product.objects.count()

