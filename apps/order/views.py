import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.adminlte.views import CommonContextMixin, CommonViewSet
from models import Order, ORDER_STATUS
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


class OrderDetailView(CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderDetailForm

    def get_object(self, queryset=None):
        obj = super(OrderDetailView, self).get_object(queryset)
        hash_code = self.kwargs.get('hash_code', None)
        if not obj.code == hash_code or not hash_code:
            raise Http404(_("No order found!"))

        return obj