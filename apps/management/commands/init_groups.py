'''
 Create initial groups + their default permissions
 Run 'manage.py validate_permissions' prior to this one if you just added new permissions.
'''
from django.contrib.auth.models import Permission, Group
from django.core import management
from django.core.management.base import BaseCommand

from core.auth_user.constant import ADMIN_GROUP, MEMBER_GROUP, FREE_MEMBER_GROUP, CUSTOMER_GROUP


class Command(BaseCommand):
    help = '''Create initial groups + their default permissions '''

    permissions = {
        # Group name
        ADMIN_GROUP: [
            # Permission codename, app name, model name
            ('add_address', 'customer', 'address'),
            ('change_address', 'customer', 'address')
        ],
        MEMBER_GROUP: [
            ('change_seller', 'member', 'seller'),
            ('view_seller', 'member', 'seller'),
            ('add_address', 'customer', 'address'),
            ('change_address', 'customer', 'address'),
            ('view_address', 'customer', 'address')
        ],
        FREE_MEMBER_GROUP: [
            ('change_seller', 'member', 'seller'),
            ('view_seller', 'member', 'seller'),
            ('add_address', 'customer', 'address'),
            ('change_address', 'customer', 'address'),
            ('view_address', 'customer', 'address')
        ],
        CUSTOMER_GROUP: [
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
