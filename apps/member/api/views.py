import ast
import logging
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response

import serializers
from ..models import Seller
from utils.api.views import PaginateMaxModelViewSet, ContentTypeObjectView


log = logging.getLogger(__name__)


class SellerViewSet(PaginateMaxModelViewSet):
    """ A viewset for viewing and editing user instances. """
    serializer_class = serializers.SellerUserSerializer
    permission_required = 'member.change_seller'
    # Exclude restframework's anonymous user which can cause 500s in url-versing due to its negative pk
    queryset = Seller.objects.exclude(username='AnonymousUser').exclude(pk__lt=0)

class Profile(generics.GenericAPIView):
    ''' Return current users's profile '''
    model = Seller
    queryset = Seller.objects.all()
    permission_required = 'member.view_seller'

    def get(self, request):
        return Response(serializers.SellerUserSerializer(request.user).data)


class GroupsAndUsersList(generics.GenericAPIView):
    '''
     List of all non-superuser users and groups. Used for multiple select widgets
     (for sharing, parenal control rules).
     Since this is not handling a single model/object, we add a custom
     has_permission method.
    '''
    permission_required = 'member.add_seller'

    def get(self, *args, **kwargs):
        users = Seller.objects.filter(is_active=True, is_superuser=False).exclude(
            username='AnonymousUser').exclude(pk__lt=0)
        if self.request.user.is_admin:
            groups = Group.objects.order_by('name')
        else:
            # f = Q(billingaccount_user__in=self.request.user.billingaccount_admin.all()) | \
            #     Q(billingaccount_user__in=self.request.user.billingaccount_user.all())
            # users = users.filter(f)
            groups = Group.objects.none()

        users = users.order_by("username")

        # For sharing widget we want to exclude the current user
        exclude_self = ast.literal_eval(self.request.GET.get('exclude_self', 'True'))
        if exclude_self:
            users = users.exclude(pk=self.request.user.pk)

        data = {
            'users': serializers.MemberUserSimpleSerializer(users, many=True).data,
            'groups': serializers.GroupSimpleSerializer(groups, many=True).data
        }

        return Response(data)
