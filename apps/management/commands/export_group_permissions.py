'''
 Custom management command to export a single group's permission set using
 natural keys.

 Careful: This will overwrite any existing record with the same pk!
 If needed modify the pk in the file by hand to avoid collision.

 Import with: ./manage.py loaddata my_group.json
'''
import logging
import datetime
from django.core.management.base import BaseCommand
from django.core import serializers
from django.contrib.auth.models import Group

log = logging.getLogger(__name__)

class Command(BaseCommand):
    args = '<group_id>'
    help = ''' Export given group's permission to json.'''

    def handle(self, *args, **options):
        group_id = args[0]
        g = Group.objects.get(pk=group_id)
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")

        with open('%s-permisions-%s.json' % (g.name.replace(' ', '_'), filename), 'w') as output:
            group_json = serializers.serialize('json', [g], indent=2, use_natural_keys=True)
            output.write(group_json)
