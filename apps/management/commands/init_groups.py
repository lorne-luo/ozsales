'''
 Create initial groups + their default permissions
 Run 'manage.py validate_permissions' prior to this one if you just added new permissions.
'''
from django.core import management
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
import copy

class Command(BaseCommand):

    help = '''Create initial groups + their default permissions '''

    permissions = {
        # Group name
        'Seller': [
            # Permission codename, app name, model name
            ('add_address', 'customer', 'address'),
            ('change_address', 'customer', 'address')
        ],
        'Customer': [
            ('add_address', 'customer', 'address'),
            ('change_address', 'customer', 'address')
        ],
        'Admin': [
            ('add_address', 'customer', 'address'),
            ('change_address', 'customer', 'address')
        ],
    }

    def handle(self, *args, **options):
        management.call_command('validate_permissions')

        for group_name, permission_set in self.permissions.items():
            group, _created = Group.objects.get_or_create(name=group_name)

            permissions = []
            not_found = []
            for codename, app_label, model_name in permission_set:
                try:
                    p = Permission.objects.get(
                        codename=codename, content_type__app_label=app_label,
                        content_type__model=model_name)
                    permissions.append(p)
                except Permission.DoesNotExist:
                    not_found.append(codename)

            print "\nGroup '%s', adding permissions: \n%s\n" \
                % (group_name, '\t' + '\n\t'.join([p.codename for p in permissions]))

            group.permissions.clear()
            group.permissions.add(*permissions)

        if not_found:
            print "Warning: Unable to find these permissions: %s" % ', '.join(not_found)


     
