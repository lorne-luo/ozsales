# coding=utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import Http404
from django.core.exceptions import PermissionDenied
from dal import autocomplete
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from apps.customer.models import Customer, CustomerCart, CartProduct, Address
from core.libs.string import include_non_asc
from core.views.permission import ProfileRequiredMixin
from ..product.models import Product


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


class CustomerAutocomplete(ProfileRequiredMixin, autocomplete.Select2QuerySetView):
    model = Customer
    paginate_by = 20
    create_field = 'name'
    profile_required = ('member.seller',)

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


class AddressAutocomplete(ProfileRequiredMixin, autocomplete.Select2QuerySetView):
    model = Address
    paginate_by = 20
    create_field = 'name'
    profile_required = ('member.seller',)

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
