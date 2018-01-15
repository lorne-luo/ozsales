import logging
from braces.views import GroupRequiredMixin
from dal import autocomplete
from django.db.models import Count, Q
from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.django.autocomplete import HansSelect2ViewMixin
from core.django.permission import ProfileRequiredMixin
from core.utils.string import include_non_asc
from core.api.permission import SellerPermissions
from core.api.views import CommonViewSet
from core.auth_user.constant import ADMIN_GROUP, MEMBER_GROUP, PREMIUM_MEMBER_GROUP
from ..models import Customer, Address, CustomerCart, CartProduct
from ...product.models import Product

import serializers

log = logging.getLogger(__name__)


class AddressViewSet(CommonViewSet):
    """api views for Address"""
    queryset = Address.objects.all()
    serializer_class = serializers.AddressSerializer
    filter_fields = ['name', 'mobile', 'address', 'customer', 'id_number']
    search_fields = ['name', 'mobile', 'address', 'customer', 'id_number']


class CustomerViewSet(GroupRequiredMixin, CommonViewSet):
    """api views for Customer"""
    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSerializer
    filter_fields = ['seller', 'name', 'email', 'mobile', 'order_count', 'primary_address',
                     'remark', 'tags']
    search_fields = ['name', 'mobile', 'primary_address__name']
    group_required = [ADMIN_GROUP, MEMBER_GROUP, PREMIUM_MEMBER_GROUP]
    permission_classes = (SellerPermissions,)

    def get_queryset(self):
        queryset = super(CustomerViewSet, self).get_queryset()
        if self.request.user.is_admin or self.request.user.is_superuser:
            return queryset
        return queryset.filter(seller=self.request.profile)




class CustomerAutocomplete(ProfileRequiredMixin, HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = Customer
    paginate_by = 20
    profile_required = ('member.seller',)

    def create_object(self, text):
        return self.get_queryset().create(**{self.create_field: text, 'seller': self.request.profile})

    def get_queryset(self):
        qs = Customer.objects.belong_to(self.request.user).annotate(
            order_count_num=Count('order')).order_by('-order_count_num')

        if include_non_asc(self.q):
            qs = qs.filter(name__icontains=self.q)
        else:
            # all ascii, number and letter
            if self.q.isdigit():
                qs = qs.filter(mobile__icontains=self.q)
            else:
                qs = qs.filter(pinyin__contains=self.q.lower())
        return qs


class AddressAutocomplete(ProfileRequiredMixin, HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = Address
    paginate_by = 20
    create_field = 'address'
    profile_required = ('member.seller',)

    def create_object(self, text):
        #todo extract name, phone number
        return self.get_queryset().create(**{self.create_field: text, 'customer_id': self.forwarded.get('customer')})

    def get_queryset(self):
        qs = Address.objects.belong_to(self.request.user)
        cid = self.forwarded.get('customer')

        if cid:
            qs = qs.filter(customer_id=cid)

        if include_non_asc(self.q):
            qs = qs.filter(Q(name__icontains=self.q) | Q(address__icontains=self.q))
        else:
            # all ascii, number and letter
            if self.q.isdigit():
                qs = qs.filter(mobile__icontains=self.q)
            else:
                qs = qs.filter(pinyin__contains=self.q.lower())
        return qs


class AddCart(GenericAPIView):
    model = CartProduct
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id', None)
        amount = request.POST.get('amount', 1)
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({'success': False, 'detail': 'Product #%s does not existed.' % product_id}, status=400)
        try:
            customer = Customer.objects.get(seller=request.user)
        except Customer.DoesNotExist:
            raise Http404

        cart, created = CustomerCart.objects.get_or_create(customer=customer)
        cart_product = cart.products.all().filter(product=product).first()
        if cart_product:
            cart_product.amount += amount
            cart_product.save(update_fields=['amount'])
        else:
            cart_product = CartProduct(product=product, amount=amount, cart=cart)
            cart_product.save()

        return Response({'success': True}, status=200)
