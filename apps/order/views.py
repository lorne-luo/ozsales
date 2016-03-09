# coding=utf-8
import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from rest_framework import permissions
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.adminlte.views import CommonContextMixin, CommonViewSet
from models import Order, ORDER_STATUS
import serializers
import forms


def change_order_status(request, order_id, status_str):
    order = get_object_or_404(Order, pk=order_id)
    order.status = status_str
    if status_str == ORDER_STATUS.FINISHED:
        if order.is_paid:
            order.finish_time = datetime.datetime.now()
            order.customer.last_order_time = order.create_time
            order.save()
            customer = order.customer
            customer.order_count += 1
            customer.save()
    else:
        order.save()
    referer = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(referer)


def change_order_paid(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_paid = True
    order.save()
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
        "all": ("order.view_order",)
    }

    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Customer', 'Paid', 'Status', 'Amount', 'Product Cost AUD', 'Shipping Fee',
                                   'Total Cost AUD', 'Total Cost RMB', 'Sell Price RMB', 'Profit RMB', '']
        context['table_fields'] = ['link', 'is_paid', 'status', 'total_amount', 'product_cost_aud', 'shipping_fee',
                                   'total_cost_aud', 'total_cost_rmb', 'sell_price_rmb', 'profit_rmb', 'id']
        return context


class OrderAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Order
    form_class = forms.OrderAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("order.add_order",)
    }

    def get_success_url(self):
        return reverse('order:order-list-short')


class OrderUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("order.change_order",)
    }

    def get_success_url(self):
        return reverse('order:order-list-short')


class OrderDetailView(CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderDetailForm

    def get_object(self, queryset=None):
        obj = super(OrderDetailView, self).get_object(queryset)
        customer_id = self.kwargs.get('customer_id', None)
        if not obj.customer_id == long(customer_id):
            raise Http404(_("No order found!"))

        return obj


from django_filters import Filter, FilterSet
from rest_framework import filters


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
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer
    filter_class = OrderFilter
    permission_classes = [permissions.DjangoModelPermissions]
    search_fields = ['customer', 'is_paid', 'status', 'ship_time', 'finish_time']
