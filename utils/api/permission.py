''' Imported from base.py, in it's own file to avoid ImportErrors. '''
import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.fields.related import ForeignKey
from rest_framework import permissions
from middleware.apps.accounts.models import OmniscreenUser


log = logging.getLogger(__name__)

class IsOwnerAdminOrSuperuser(permissions.DjangoObjectPermissions):
    """
     Object views: Allow superusers, admin and the object owner, if
     object has no owner, based on model permissions

     List views: Allow superusers, admin and others based on their
     model permissions.
    """

    # Adding 'view' permissions.
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def _log_model_permissions(self, request, view, obj=None):
        ''' For debug purpose only '''
        if obj:
            model_cls = obj.__class__
        else:
            if callable(getattr(view, 'has_permission', False)):
                log.debug("%s.has_permission(): %s" % (
                          view.__class__.__name__, view.has_permission(request, view)))
                return

            elif hasattr(view, 'custom_permissions'):
                log.debug("View has custom permissions: %s" %
                          self._determine_custom_permissions(request, view.custom_permissions))
                return

            model_cls = getattr(view, 'model', None)
            queryset = getattr(view, 'queryset', None)
            if not queryset and not model_cls:
                log.warning('%s: View does not specify queryset or model. Cannot figure out model permissions.' % view)
                return
            elif not model_cls:
                model_cls = queryset.model

        model_perms = self.get_required_permissions(request.method, model_cls)
        log.debug('has model permissions %s: %s' % (
            model_perms, request.user.has_perms([])
        ))

    def _get_related_user(self, obj):
        '''
         Search for FK to user model and return user instance or False if no FK.
         This can lead to wrong results when the model has more than one user FK.
        '''
        for f in obj.__class__._meta.fields:
            if isinstance(f, ForeignKey) and f.rel.to == OmniscreenUser:
                return getattr(obj, f.name)
        return False

    def _is_admin(self, user):
        ''' True for users of at least admin level. '''
        is_admin = bool(user) and user.is_authenticated() and user.is_admin()
        if is_admin:
            log.debug('User is admin user. Access granted')
        return is_admin

    def _get_object(self, request, view):
        '''
         When view was identified as single-object view, this will take over
         to identify the object and check object permission.
        '''

        # Custom views like for sharing which have pk and content_type in the url
        if all((a in view.kwargs for a in ('pk', 'content_type'))):
            content_type = ContentType.objects.get(model=view.kwargs.get('content_type'))
            queryset = content_type.model_class().objects
            model_name = content_type.model_class().__name__
        # Views which specify a model/queryset/get_queryset = ...
        elif callable(getattr(view, 'get_queryset', False)):
            queryset = view.get_queryset()
            model_name = queryset.model.__name__
        else:
            raise RuntimeError('Unable to determine object permission, no \
                queryset/model or contenttype information found.')

        try:
            obj = queryset.get(pk=view.kwargs['pk'])
        except ObjectDoesNotExist:
            log.debug("Object with pk %s of class %s not in view's queryset. Access denied." %
                      (view.kwargs['pk'], model_name))
            return None
        return obj

    def _determine_custom_permissions(self, request, custom_permissions):
        '''
         Determines view's custom permission. Accepts single, multi or
         method-to-perm mapping dictionary.
        '''
        if type(custom_permissions) in (str, list, tuple):
            # e.g. 'accounts.can_share' or ['accounts.can_share', 'accounts.can_foo']
            if isinstance(custom_permissions, str):
                custom_permissions = [custom_permissions]

        elif isinstance(custom_permissions, dict):
            # e.g. {'GET': ['accounts.can_share', 'accounts.can_foo']}
            try:
                custom_permissions = custom_permissions.get(request.method)
            except KeyError:
                raise RuntimeError("Custom permission does not hold key for: %s" %
                                   request.method)
            custom_permissions = self._determine_custom_permissions(request, custom_permissions)
        else:
            raise RuntimeError("Unknown type of custom permission: '%s'" %
                               type(custom_permissions))

        return custom_permissions

    def _check_custom_permissions(self, request, view):
        ''' Check if user has custom permissions of current view. '''
        # Note: _get_custom_permissions will always convert it to a list of perms
        return request.user.has_perms(self._determine_custom_permissions(request, view.custom_permissions))

    def has_permission(self, request, view):
        ''' Called for list and detail views. '''
        obj = None
        # Don't allow anonymous access
        if not request.user.is_authenticated():
            return False

        allow = self._is_admin(request.user)
        if not allow:
            # In order of priority:
            if callable(getattr(view, 'has_permission', False)): # a) View has a own has_permission method
                allow = view.has_permission(request, view)
                if allow is None:
                    # If it returns None, fall back to model permissions
                    allow = super(IsOwnerAdminOrSuperuser, self).has_permission(request, view)

            elif hasattr(view, 'custom_permissions'): # b) View specifies a custom permission
                allow = self._check_custom_permissions(request, view)
            elif 'pk' in view.kwargs:
                # c) Single-object view, let has_object_permission figure it out:
                obj = self._get_object(request, view)
                if obj:
                    allow = self.has_object_permission(request, view, obj)
                else:
                    allow = False

            else: # d) List view/anything else, let ModelPermissions figure it out:
                allow = super(IsOwnerAdminOrSuperuser, self).has_permission(request, view)

            self._log_model_permissions(request, view, obj)
            log.debug('has_permission: %s' % allow)
        return allow

    def has_object_permission(self, request, view, obj):
        '''
         Has user FK: owner only (will try to cast to child-class, see cast()
                                  method of model Video)
         Has no user FK: based on model permissions.
        '''
        allow = self._is_admin(request.user)
        if not allow:
            # Cast to child-class if it has one
            if callable(getattr(obj, 'cast', False)):
                obj = obj.cast()

            owner = self._get_related_user(obj) # False if no user fk, None if no user set
            if owner != False: # Does object have user fk?
                allow = owner == request.user
            else: # model without owner, allow according to ModelPermissions
                allow = super(IsOwnerAdminOrSuperuser, self).has_permission(request, view)
            log.debug('has_object_permission for %s pk %s: %s'
                      % (obj.__class__.__name__, obj.pk, allow))
        return allow
