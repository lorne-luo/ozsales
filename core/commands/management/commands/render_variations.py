import os

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.db.models import FileField

from apps.customer.models import Address
from apps.product.models import Product
from apps.tenant.models import Tenant


class Command(BaseCommand):
    help = "This command regenerate all thumbnail pictures"

    def add_arguments(self, parser):
        parser.add_argument(
            '--r',
            action='store_true',
            dest='replace',
            default=False,
            help='Force replace thumbnail pics',
        )

    def handle(self, *args, **options):
        replace = options['replace']

        for tenant in Tenant.objects.normal():
            tenant.set_schema()

            for a in Address.objects.all():
                try:
                    if a.id_photo_front:
                        a.id_photo_front.render_variations(replace)
                        self.stdout.write(str(a.id_photo_front))
                    if a.id_photo_back:
                        a.id_photo_back.render_variations(replace)
                        self.stdout.write(str(a.id_photo_back))
                except Exception as ex:
                    self.stdout.write('Address#%s err: %s' % (a.id, ex))

            for p in Product.objects.all():
                try:
                    if p.pic:
                        p.pic.render_variations(replace)
                        self.stdout.write(str(p.pic))
                except Exception as ex:
                    self.stdout.write('Product#%s err: %s' % (p.id, ex))
