from django.core.management.base import BaseCommand

from djstripe.models import Plan
from django.db import connection

from apps.order.models import OrderProduct
from apps.product.models import Product


class Command(BaseCommand):
    help = "output price table."

    def handle(self, *args, **options):
        connection.set_schema('t3')

content = '''| Picture        | Product           | Price  |
| ------------- |:-------------:| -----:|\n'''

for p in Product.objects.all().order_by('brand_cn', 'brand_en'):
    last_order = OrderProduct.objects.filter(product=p).order_by('-create_time').first()
    if last_order:
        url = 'http://s.luotao.net' + p.pic.thumbnail.url if p.pic else ''
        content += ('|![](%s)|%s|%s|\n' % (
            url, str(p).strip(), last_order.sell_price_rmb))
        # content += ('|<img src="%s" width="200">|%s|%s|\n' % (
        #     url, str(p).strip(), last_order.sell_price_rmb))

print(content)
