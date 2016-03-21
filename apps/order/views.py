# coding=utf-8
import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django_filters import Filter, FilterSet
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from rest_framework import permissions
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.adminlte.views import CommonContextMixin, CommonViewSet
from models import Order, ORDER_STATUS
from ..member.models import Seller
import serializers
import forms


def change_order_status(request, order_id, status_value):
    order = get_object_or_404(Order, pk=order_id)
    order.set_status(status_value)
    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer)


def change_order_paid(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.set_paid()
    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer)


class OrderIndex(MultiplePermissionsRequiredMixin, TemplateView):
    ''' List of order. '''
    template_name = 'order/order-list.html'
    permissions = {
        "any": ("order.add_order", "order.view_order")
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['processing_orders'] = Order.objects.exclude(status=ORDER_STATUS.FINISHED).order_by('-id')
        context['finished_orders'] = Order.objects.filter(status=ORDER_STATUS.FINISHED).order_by('-id')
        return self.render_to_response(context)


class OrderAddEdit(MultiplePermissionsRequiredMixin, TemplateView):
    ''' Add/Edit a order. '''
    template_name = 'order/order-edit.html'
    permissions = {
        "any": ("order.add_order", "order.view_order")
    }

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        context = {'form': forms.OrderForm2(), }
        if pk:
            order = get_object_or_404(Order, id=pk)
            context['order'] = order

        return self.render_to_response(context)


class OrderListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Order
    template_name_suffix = '_list'  # order/order_list.html
    permissions = {
        "all": ("order.is_superuser",)
    }

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Create Time', 'Customer', 'Amount', 'Status', 'Paid', 'Price', 'Shipping', '']
        context['table_fields'] = ['link', 'is_paid', 'status', 'total_amount', 'product_cost_aud', 'shipping_fee',
                                   'total_cost_aud', 'total_cost_rmb', 'sell_price_rmb', 'profit_rmb', 'id']
        return context


class OrderAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Order
    form_class = forms.OrderAddForm
    # template_name = 'adminlte/common_form.html'
    template_name = 'order/order_form.html'
    permissions = {
        "all": ("order.add_order",)
    }

    def get_success_url(self):
        return reverse('order:order-list-short')

    def get_context_data(self, **kwargs):
        context = super(OrderAddView, self).get_context_data(**kwargs)
        context['new_product_form'] = forms.OrderProductInlineAddForm()
        return context


class OrderUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderUpdateForm
    template_name = 'order/order_form.html'
    permissions = {
        "all": ("order.change_order",)
    }

    def get_success_url(self):
        return reverse('order:order-list-short')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)

        context['product_forms'] = [forms.OrderProductInlineAddForm(instance=product)
                                    for product in self.object.products.all()]

        context['new_product_form'] = forms.OrderProductInlineAddForm()
        return context


class OrderDetailView(CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderDetailForm

    def get_template_names(self):
        if self.request.user.is_superuser:
            return 'order/order_detail_admin.html'
        else:
            return 'order/order_detail.html'

    def get_object(self, queryset=None):
        obj = super(OrderDetailView, self).get_object(queryset)
        customer_id = self.kwargs.get('customer_id', None)
        if not obj.customer_id == long(customer_id):
            raise Http404(_("No order found!"))

        return obj


class ListFilter(Filter):
    def filter(self, qs, value):
        self.lookup_type = 'in'
        values = value.split(',')
        return super(ListFilter, self).filter(qs, values)


class OrderFilter(FilterSet):
    status_in = ListFilter(name='status')

    class Meta:
        model = Order
        fields = ['status_in', 'customer', 'is_paid', 'status', 'ship_time', 'finish_time']


# api views for Order

class OrderViewSet(CommonViewSet):
    serializer_class = serializers.OrderSerializer
    filter_class = OrderFilter
    permission_classes = [permissions.DjangoModelPermissions]
    search_fields = ['customer__name', 'status']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        elif self.request.user.is_authenticated():
            return Order.objects.filter(customer__seller=self.request.user)
        else:
            return Order.objects.none()


class OrderMemberListView(CommonContextMixin, ListView):
    model = Order
    template_name_suffix = '_member_list'  # order/order_member_list.html

    def get_context_data(self, **kwargs):
        context = super(OrderMemberListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Create Time', 'Customer', 'Amount', 'Status', 'Paid', 'Price', 'Shipping', '']
        context['table_fields'] = ['link', 'is_paid', 'status', 'total_amount', 'product_cost_aud', 'shipping_fee',
                                   'total_cost_aud', 'total_cost_rmb', 'sell_price_rmb', 'profit_rmb', 'id']
        return context

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username', None)

        try:
            user = Seller.objects.get(username=username)
            user.backend = settings.AUTHENTICATION_BACKENDS[0]

            if user and not user.is_superuser:
                if user.is_active:
                    login(request, user)
            else:
                raise Http404
        except Seller.DoesNotExist:
            raise Http404

        return super(OrderMemberListView, self).get(self, request, *args, **kwargs)
