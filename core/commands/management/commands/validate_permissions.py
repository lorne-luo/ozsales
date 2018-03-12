'''
 Custom management command to a) create new custom permissions defined in the meta
 classes + a view permission, b) delete stale ones and c) update
 names/descriptions of existing ones independent from south/syncdb.

 To create a view permission for each model, un-comment the calls to
 self._add_view_permission()

 South might handle this better soon: http://south.aeracode.org/ticket/211
'''
from operator import __or__

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.apps import apps
from django.contrib.auth import management
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):

    help = '''Deletes stale permissions, creates
        non-existing, updates names.'''

    def handle(self, *args, **options):
        # Don't exclude models without permissions here, as it would not delete
        # stale ones if all get removed at once:
        for model in apps.get_models():
            content_type = ContentType.objects.get_for_model(model)
            # This will raise an exception if 2 permissions have same codename:
            try:
                _all_permissions = management._get_all_permissions(model._meta)
            except ValueError as e:
                if str(e) == 'too many values to unpack':
                    print "Error: Check permissions tuple of '%s', missing a comma? " % model.__name__, \
                          "Make sure the surrounding tuple has a trailing comma if it holds only a single permission."
                    return
                else:
                    raise

            self._create_non_existing_permissions(model, content_type)
            # self._delete_stale_permissions(model, content_type) # not work with proxy models
            self._update_changed_names(model, content_type)

    def _add_view_permission(self, permissions, model_name):
        '''
         Add permission tuple in same format as we would define it in the
         meta class.
        '''
        permissions = list(permissions)
        view_permission = ('view_%s' % model_name.lower(), 'Can view %s' % model_name.lower())
        if not view_permission in permissions:
            permissions.append(view_permission)
        return permissions

    def _create_non_existing_permissions(self, model, content_type):
        '''
         Creates custom permissions from the Meta class which do not exist
         in the database yet + a view_modelname permission.
        '''

        permissions = (management._get_builtin_permissions(model._meta) +
            list(model._meta.permissions))
        permissions = self._add_view_permission(permissions, content_type.model)

        for codename, name in permissions:
            # These filter may not check for the name, as that would lead to
            # permissions where only the name was changed, being recreated.
            permission, created = Permission.objects.get_or_create(
                content_type=content_type,
                codename=codename)
            if created:
                permission.name = name
                permission.save()
                print "Created permission '%s' on model %s" % (codename, model)

    def _delete_stale_permissions(self, model, content_type):
        '''
         Deletes custom permissions which do no longer exist in the Meta
         class.
        '''
        # Have to include the default Django change/add/delete ones as those
        # should never be deleted.
        permissions = (management._get_builtin_permissions(model._meta) +
            list(model._meta.permissions))
        permissions = self._add_view_permission(permissions, content_type.model)

        # These filter may not check for the name, as that would delete
        # permissions where only the name was changed.
        non_stale = reduce(__or__, (Q(codename=c) for c, n in permissions))

        stale_permissions = Permission.objects.filter(content_type=content_type) \
            .exclude(non_stale)

        if stale_permissions:
            for p in stale_permissions:
                print "Deleted stale permission '%s' on model %s" % (p.codename,
                                                                     model)
            stale_permissions.delete()

    def _update_changed_names(self, model, content_type):
        '''
         Updates names of custom permissions in the database when they no
         longer match the name in the Meta class.
        '''
        for codename, name in model._meta.permissions:
            permission = Permission.objects.get(content_type=content_type,
                                                codename=codename)

            if permission.name != name:
                permission.name = name
                permission.save()

                print "Updated name for '%s' on model %s to '%s'" \
                    % (permission.codename, model, name)
