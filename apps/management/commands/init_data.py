'''
 Create initial common data 
'''
from django.core import management
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
import copy
from apps.product.models import Country


class Command(BaseCommand):
    help = '''Create initial common data '''

    countries = {
        'China': 'CN',
        'Australia': 'AU',
        'American': 'US',
        'Great British': 'UK',
        'Japan': 'JP',
        'Germany': 'DE',
    }

    # todo brand
    # todo product category
    # todo interest tags

    def handle(self, *args, **options):

        for full_name, short_name in self.countries.items():
            if not Country.objects.filter(name=full_name).count():
                c = Country(name=full_name, short_name=short_name)
                c.save()
                print '\t%s  (%s)\t\tCreated' % (full_name, short_name)


     
