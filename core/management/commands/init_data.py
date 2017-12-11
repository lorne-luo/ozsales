'''
 Create initial common data 
'''
from django.core import management
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
import copy


class Command(BaseCommand):
    help = '''Create initial common data '''

    # todo brand
    # todo product category
    # todo interest tags

    def handle(self, *args, **options):
        pass


     
