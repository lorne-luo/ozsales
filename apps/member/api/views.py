import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.sms.verification import send_verification_code
from . import serializers
from core.api.permission import AdminOnlyPermissions
from ..models import Seller
from utils.api.views import PaginateMaxModelViewSet

log = logging.getLogger(__name__)


class SellerViewSet(PaginateMaxModelViewSet):
    """ A viewset for viewing and editing user instances. """
    serializer_class = serializers.SellerSerializer
    permission_classes = [AdminOnlyPermissions]
    # Exclude restframework's anonymous user which can cause 500s in url-versing due to its negative pk
    queryset = Seller.objects.exclude(pk__lt=1)
    filter_fields = ['name', 'primary_currency', 'auth_user']
    search_fields = ['name', 'primary_currency']
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)


class Profile(generics.GenericAPIView):
    ''' Return current users's profile '''
    model = Seller
    queryset = Seller.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(serializers.SellerSerializer(request.profile).data)


class SendVerificationCode(APIView):
    permission_classes = [AllowAny]

    def post(self, request, **kwargs):
        mobile = request.POST.get('mobile')
        if mobile:
            success, detail = send_verification_code(mobile)
            return Response({'success': success, 'detail': detail})
        else:
            return Response({'success': False, 'detail': '请提供中国或澳洲手机号码'})
