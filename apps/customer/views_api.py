# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db import transaction
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.views.views import CommonContextMixin, CommonViewSet
from models import Customer, CustomerCart, CartProduct
from ..product.models import Product
import serializers
import forms


class AddCart(GenericAPIView):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id', None)
        amount = request.POST.get('amount', 1)

        product = Product.objects.get(pk=product_id)
        customer = Customer.objects.get(seller=request.user)
        cart = CustomerCart.objects.get_or_create(customer=customer)
        cart_product = cart.products.all().filter(product=product).first()
        if cart_product:
            cart_product.amount += amount
            cart_product.save(update_fields=['amount'])
        else:
            cart_product = CartProduct(product=product, amount=amount, cart=cart)
            cart_product.save()

        success = True
        detail = None

        return Response({'success': success, 'detail': detail}, status=200)
