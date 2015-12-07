''' Imported from base.py, in it's own file to avoid ImportErrors. '''
import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.db.models.fields.related import ForeignKey
from rest_framework import permissions
from apps.member.models import Seller

log = logging.getLogger(__name__)


class AdminOnlyPermissions(permissions.DjangoModelPermissions):

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        if request.user.is_admin:
            return True
        return False

class ModelPermissions(permissions.DjangoObjectPermissions):
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

    def _get_object(self, request, view):
        '''
         When view was identified as single-object view, this will take over
         to identify the object and check object permission.
        '''

        # Custom views like for sharing which have pk and content_type in the url
        if all((a in view.kwargs for a in ('pk', 'content_type_name'))):
            content_type = ContentType.objects.get(model=view.kwargs.get('content_type_name'))
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
            if obj:
                setattr(view, 'queryset', queryset)  # important! so the super has_permision() can check model permisson
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
        if not request.user.is_authenticated():
            return False

        if request.user.is_admin:
            return True

        if callable(getattr(view, 'has_permission', False)):  # a) View has a own has_permission method
            return view.has_permission(request, view)


        if hasattr(view, 'custom_permissions'):  # b) View specifies a custom permission
            if self._check_custom_permissions(request, view):
                return True

        # for some ContentTypeObjectView like tags.views.ReadSetTags, check model permission need model name
        if not hasattr(view, 'model') and not hasattr(view, 'queryset'):
            obj = self._get_object(request, view) # will set view.queryset

        return super(ModelPermissions,self).has_permission( request, view)

class ObjectPermissions(ModelPermissions):
    """
     object level permission
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

    def _get_related_user(self, obj):
        '''
         Search for FK to user model and return user instance or False if no FK.
         This can lead to wrong results when the model has more than one user FK.
        '''
        for f in obj.__class__._meta.fields:
            if isinstance(f, ForeignKey) and f.rel.to == Seller:
                return getattr(obj, f.name)
        return False

    def has_permission(self, request, view):
        ''' Called for list and detail views. '''
        obj = None
        # Don't allow anonymous access
        if not request.user.is_authenticated():
            return False

        if self._is_admin(request.user):
            return True

        if callable(getattr(view, 'has_permission', False)):  # a) View has a own has_permission method
            if view.has_permission(request, view):
                return True

        if hasattr(view, 'custom_permissions'):  # b) View specifies a custom permission
            if self._check_custom_permissions(request, view):
                return True

        # for some ContentTypeObjectView like tags.views.ReadSetTags, check model permission need model name
        if not hasattr(view, 'model') and not hasattr(view, 'queryset'):
            obj, content_type = view.identify_object()
            if obj:
                view.model = obj._meta.model

        if super(ObjectPermissions, self).has_permission(request, view):  # check model permission
            return True
        elif 'pk' in view.kwargs:
            # Single-object view, let has_object_permission figure it out:
            if not obj:
                obj = self._get_object(request, view)

            if obj and self.has_object_permission(request, view, obj):
                return True

        log.debug('has_permission: %s' % False)
        return False

    def has_object_permission(self, request, view, obj):
        '''
         Has user FK: owner only (will try to cast to child-class, see cast()
                                  method of model Video)
         Has no user FK: based on model permissions.
        '''

        if self._is_admin(request.user):
            return True

        # if have model permission, will not check obj permission
        model_perms = self.get_required_object_permissions(request.method, obj._meta.model)
        if request.user.has_perms(model_perms):
            return True

        obj_casted = None
        if callable(getattr(obj, 'cast', False)):
            obj_casted = obj.cast()

        # must check ownership before calling super.has_object_permission
        owner = self._get_related_user(obj_casted) if obj_casted else self._get_related_user(obj)
        # False if no user fk, None if no user set
        if owner != False and owner == request.user:  # Does object have user fk?
            return True

        # obj is this user
        if request.user == obj or request.user == obj_casted:
            return True

        # check obj permission again after casted
        if self.check_object_permissions(request, obj):
            return True

        # check obj_casted permission
        if obj_casted and obj != obj_casted:
            if self.check_object_permissions(request, obj_casted):
                return True

        # have on obj permission, deny this request
        # if have read (GET method) permission raise 404 otherwise return false(403)
        if request.method.upper() == 'GET':
            raise Http404
        else:
            read_perms = self.get_required_object_permissions('GET', obj._meta.model)
            if not request.user.has_perms(read_perms, obj):
                raise Http404

        return False

    def check_object_permissions(self, request, obj):
        model = obj._meta.model
        perms = self.get_required_object_permissions(request.method, model)
        if request.user.has_perms(perms, obj):
            return True
        return False
