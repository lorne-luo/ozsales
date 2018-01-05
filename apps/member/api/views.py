import logging
from rest_framework import generics
from rest_framework.response import Response

import serializers
from ..models import Seller
from utils.api.views import PaginateMaxModelViewSet

log = logging.getLogger(__name__)


class SellerViewSet(PaginateMaxModelViewSet):
    """ A viewset for viewing and editing user instances. """
    serializer_class = serializers.SellerSerializer
    permission_required = 'member.change_seller'
    # Exclude restframework's anonymous user which can cause 500s in url-versing due to its negative pk
    queryset = Seller.objects.exclude(pk__lt=0)


class Profile(generics.GenericAPIView):
    ''' Return current users's profile '''
    model = Seller
    queryset = Seller.objects.all()
    permission_required = 'member.view_seller'

    def get(self, request):
        return Response(serializers.SellerSerializer(request.profile).data)
