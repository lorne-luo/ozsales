# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponseRedirect
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.views.views import CommonContextMixin, CommonViewSet
from models import ExpressCarrier, ExpressOrder
from ..order.models import ORDER_STATUS
import serializers
import forms


# views for ExpressCarrier

class ExpressCarrierListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = ExpressCarrier
    template_name_suffix = '_list'  # express/expresscarrier_list.html
    permissions = {
        "all": ("express.view_expresscarrier",)
    }


class ExpressCarrierAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("express.add_expresscarrier",)
    }


class ExpressCarrierUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("express.change_expresscarrier",)
    }


class ExpressCarrierDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = ExpressCarrier
    form_class = forms.ExpressCarrierDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("express.view_expresscarrier",)
    }


class ExpressCarrierViewSet(CommonViewSet):
    """ api views for ExpressCarrier """
    queryset = ExpressCarrier.objects.all()
    serializer_class = serializers.ExpressCarrierSerializer
    filter_fields = ['name_cn', 'name_en', 'website', 'search_url', 'rate', 'is_default']
    search_fields = ['name_cn', 'name_en', 'website', 'search_url', 'rate', 'is_default']


# # views for ExpressOrder
#
# class ExpressOrderListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
#     model = ExpressOrder
#     template_name_suffix = '_list'  # express/expressorder_list.html
#     permissions = {
#         "all": ("express.view_expressorder",)
#     }
#
#
# class ExpressOrderAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
#     model = ExpressOrder
#     form_class = forms.ExpressOrderAddForm
#     template_name = 'adminlte/common_form.html'
#     permissions = {
#         "all": ("expressorder.add_expressorder",)
#     }
#
#
# class ExpressOrderUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
#     model = ExpressOrder
#     form_class = forms.ExpressOrderUpdateForm
#     template_name = 'adminlte/common_form.html'
#     permissions = {
#         "all": ("expressorder.change_expressorder",)
#     }
#
#
# class ExpressOrderDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
#     model = ExpressOrder
#     form_class = forms.ExpressOrderDetailForm
#     template_name = 'adminlte/common_detail_new.html'
#     permissions = {
#         "all": ("expressorder.view_expressorder",)
#     }


# api views for ExpressOrder
class ExpressOrderViewSet(CommonViewSet):
    """ api views for ExpressOrder """
    queryset = ExpressOrder.objects.all()
    serializer_class = serializers.ExpressOrderSerializer
    # filter_class = OrderFilter
    filter_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']
    search_fields = ['carrier__name_cn', 'carrier__name_en', 'track_id', 'address__name', 'order__customer__name']


def changjiang_view(request):
    url_template = 'http://www.changjiangexpress.com/Home/Query?numbers=%s'
    changjiang_carrier = ExpressCarrier.objects.get(name_cn=u'长江快递')
    orders = ExpressOrder.objects.filter(carrier=changjiang_carrier).exclude(order__status=ORDER_STATUS.FINISHED)

    order_id = ''
    for o in orders:
        order_id += o.track_id if not order_id else '%0A' + o.track_id

    return HttpResponseRedirect(url_template % order_id)
