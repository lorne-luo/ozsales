import logging

from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework.permissions import DjangoModelPermissions, BasePermission
from core.auth_user.constant import MEMBER_GROUP, CUSTOMER_GROUP, PREMIUM_MEMBER_GROUP

log = logging.getLogger(__name__)


# add below in settings
#
# 'DEFAULT_PERMISSION_CLASSES': [
#         'core.api.permission.CommonAPIPermissions',
#     ],

class ForbiddenAny(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class AdminOnlyPermissions(DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        if request.user.is_admin or request.user.is_superuser:
            return True
        return False


class ModelPermissions(DjangoModelPermissions):
    """
     model level permission
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

    def _determine_custom_permissions(self, request, custom_permissions):
        """
         Determines view's custom permission. Accepts single, multi or
         method-to-perm mapping dictionary.
        """
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
        """ Check if user has custom permissions of current view. """
        # Note: _get_custom_permissions will always convert it to a list of perms
        return request.user.has_perms(self._determine_custom_permissions(request, view.custom_permissions))

    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            return False

        if request.user.is_admin:
            return True

        if callable(getattr(view, 'has_permission', False)):  # a) View has a own has_permission method
            custom_has_permission = view.has_permission(request, view)
            if custom_has_permission is not None:  # if return None continue to check obj level permission
                return custom_has_permission

        if hasattr(view, 'custom_permissions'):  # b) View specifies a custom permission
            if self._check_custom_permissions(request, view):
                return True

        return super(ModelPermissions, self).has_permission(request, view)


class ObjectPermissions(ModelPermissions):
    """
     object level permission
    """

    def _check_owner(self, user, obj):
        """
         check whether user own this obj
        """
        if hasattr(obj, 'owner') and isinstance(getattr(obj, 'owner'), get_user_model()):
            if user == getattr(obj, 'owner'):
                return True
        if hasattr(obj, 'user') and isinstance(getattr(obj, 'user'), get_user_model()):
            if user == getattr(obj, 'user'):
                return True
        return False

    def has_object_permission(self, request, view, obj):
        """
         Has user FK: owner only (will try to cast to child-class, see cast()
                                  method of abstract model)
         Has no user FK: based on model permissions.
        """
        # Don't allow anonymous access
        if not request.user.is_authenticated():
            return False

        if request.user.is_admin:
            return True

        # if have model permission, will not check obj permission
        model_perms = self.get_required_object_permissions(request.method, obj._meta.model)
        if request.user.has_perms(model_perms):
            return True

        obj_casted = None
        if callable(getattr(obj, 'cast', False)):
            obj_casted = obj.cast()

        # if user own this obj
        if self._check_owner(request.user, obj):
            return True
        if obj_casted and self._check_owner(request.user, obj_casted):
            return True

        # obj is this user
        if request.user == obj or request.user == obj_casted:
            return True

        # check obj permission again after casted
        if self.check_permissions(request, obj):
            return True

        # check obj_casted permission
        if obj_casted and obj != obj_casted:
            if self.check_permissions(request, obj_casted):
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

    def check_permissions(self, request, obj):
        model = obj._meta.model
        perms = self.get_required_object_permissions(request.method, model)
        if request.user.has_perms(perms, obj):
            return True
        return False


class CommonAPIPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


# ================================ customized ============================

class ProfilePermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_admin or request.user.is_superuser:
            return True
        if getattr(request.user, 'profile'):
            return True
        return False


class SellerPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_admin or request.user.is_superuser or request.user.is_seller:
            return True
        return False


class CustomerPermissions(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_admin or request.user.is_superuser or request.user.is_customer:
            return True
        return False


class AbstractGroupPermissions(BasePermission):
    group_required = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_admin or request.user.is_superuser:
            return True
        user_groups = request.user.groups.values_list("name", flat=True)
        return set(self.group_required).intersection(set(user_groups))


class MemberGroupPermissions(BasePermission):
    group_required = (MEMBER_GROUP,)


class PremiumMemberGroupPermissions(BasePermission):
    group_required = (PREMIUM_MEMBER_GROUP,)


class CustomerGroupPermissions(BasePermission):
    group_required = (CUSTOMER_GROUP,)
