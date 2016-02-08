import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from models import Order, ORDER_STATUS


def change_order_status(request, order_id, status_str):
    order = get_object_or_404(Order, pk=order_id)
    order.status = status_str
    if status_str == ORDER_STATUS.FINISHED:
        if order.is_paid:
            order.finish_time = datetime.datetime.now()
            order.customer.last_order_time = order.create_time
            order.customer.order_count += 1
            order.save()
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
