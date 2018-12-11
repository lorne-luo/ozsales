import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.auth_user.models import AuthUser
from core.sms.verification import send_verification_code
from core.api.permission import AdminOnlyPermissions
from ..models import Seller
from . import serializers
from utils.api.views import PaginateMaxModelViewSet
from core.aliyun.sms.service import validate_cn_mobile
from core.sms.telstra_api_v2 import validate_au_mobile

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
        mobile = request.POST.get('mobile', '')
        mobile = validate_cn_mobile(mobile) or validate_au_mobile(mobile)
        if not mobile:
            return Response({'success': False, 'detail': '请输入正确的中国或澳洲手机号码'})

        if AuthUser.objects.filter(mobile=mobile).exists():
            return Response({'success': False, 'detail': '此号码已注册，请直接登录'})

        success, detail = send_verification_code(mobile)
        return Response({'success': success, 'detail': detail})
