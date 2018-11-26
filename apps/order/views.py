# coding=utf-8
from braces.views import MultiplePermissionsRequiredMixin
from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, ListView, CreateView, UpdateView

from core.django.permission import SellerOwnerOnlyRequiredMixin, SellerRequiredMixin
from core.django.views import CommonContextMixin, TenantPublicViewMixin
from .models import Order, ORDER_STATUS, OrderProduct
from ..customer.models import Customer
from ..express.views import CarrierInfoRequiredMixin
from ..express.forms import ExpressOrderFormSet, ExpressOrderInlineEditForm
from ..member.models import Seller
from . import forms


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
        context['processing_orders'] = Order.objects.exclude(status=ORDER_STATUS.FINISHED).order_by('-create_time')
        context['finished_orders'] = Order.objects.filter(status=ORDER_STATUS.FINISHED).order_by('-create_time')
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
            order = get_object_or_404(Order, pk=pk)
            context['order'] = order

        return self.render_to_response(context)


class OrderListView(CarrierInfoRequiredMixin, SellerRequiredMixin, CommonContextMixin, ListView):
    model = Order
    template_name_suffix = '_list'  # order/order_list.html

    def get_context_data(self, **kwargs):
        self.prompt_incomplete_carrier()
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['expressorder_form'] = ExpressOrderInlineEditForm()
        context['orderproduct_form'] = forms.OrderProductFormForList()
        return context


class OrderMemberListView(CommonContextMixin, ListView):
    model = Order
    template_name_suffix = '_member_list'  # order/order_member_list.html

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username', None)

        try:
            user = Seller.objects.get(username=username)
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            if user and not user.is_superuser:
                if user.is_active:
                    login(request, user)
            else:
                raise Http404
        except Seller.DoesNotExist:
            raise Http404

        return super(OrderMemberListView, self).get(self, request, *args, **kwargs)


class OrderAddView(SellerRequiredMixin, CommonContextMixin, CreateView):
    model = Order
    form_class = forms.OrderAddForm
    # template_name = 'adminlte/common_form.html'
    template_name = 'order/order_add.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            url = reverse('order:order-add-detail', args=[form.instance.customer_id])
            return HttpResponseRedirect(url)
        else:
            return self.form_invalid(form)


class OrderUpdateView(SellerOwnerOnlyRequiredMixin, CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderUpdateForm
    template_name = 'order/order_form.html'
    products_prefix = 'products'
    express_orders_prefix = 'express_orders'

    def get_success_url(self):
        if '_continue' in self.request.POST and self.object:
            return reverse('order:order-update', args=[self.object.pk])
        else:
            return reverse('order:order-list-short')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        instance = getattr(self, 'object')

        if self.request.POST:
            context['product_formset'] = forms.OrderProductFormSet(self.request.POST, self.request.FILES,
                                                                   prefix=self.products_prefix,
                                                                   instance=instance)
            context['express_formset'] = ExpressOrderFormSet(self.request.POST, self.request.FILES,
                                                             prefix=self.express_orders_prefix,
                                                             instance=instance)
        else:
            context['product_formset'] = forms.OrderProductFormSet(prefix=self.products_prefix, instance=instance)

            context['express_formset'] = ExpressOrderFormSet(prefix=self.express_orders_prefix, instance=instance)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data(form=form)
        product_formset = context['product_formset']
        express_formset = context['express_formset']

        product_formset_valid = product_formset.is_valid()
        express_formset_valid = express_formset.is_valid()
        if form.is_valid() and product_formset_valid and express_formset_valid:
            try:
                with transaction.atomic():
                    result = self.form_valid(form)
                    product_formset.instance = self.object
                    product_formset.save()
                    express_formset.instance = self.object
                    express_formset.save()
                    return result
            except Exception as ex:
                # from invalid
                form.add_error(None, str(ex))
                messages.error(self.request, str(ex))
                return self.render_to_response(context)
        else:
            # from invalid
            return self.render_to_response(context)


class OrderAddDetailView(OrderUpdateView):
    def get_object(self, queryset=None):
        try:
            object = super(OrderAddDetailView, self).get_object()
        except:
            object = Order(customer_id=self.kwargs['customer_id'])
            object.address_id = self.request.POST['address']
            object.seller = self.request.profile
            object.save()
        return object

    def get(self, request, *args, **kwargs):
        customer_id = kwargs['customer_id']
        if not Customer.objects.filter(pk=customer_id).exists():
            return HttpResponseRedirect(reverse('order:order-add'))

        self.object = Order(customer_id=customer_id, seller=self.request.profile)
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        context = self.get_context_data(form=form)
        product_formset = context['product_formset']
        express_formset = context['express_formset']

        product_formset_valid = product_formset.is_valid()
        express_formset_valid = express_formset.is_valid()
        if form.is_valid() and product_formset_valid and express_formset_valid:
            try:
                with transaction.atomic():
                    result = self.form_valid(form)
                    product_formset.instance = self.object
                    product_formset.save()
                    express_formset.instance = self.object
                    express_formset.save()
                    return result
            except Exception as ex:
                # from invalid
                form.add_error(None, str(ex))
                messages.error(self.request, str(ex))
                return self.render_to_response(context)
        else:
            # from invalid
            return self.render_to_response(context)


class OrderDetailView(TenantPublicViewMixin, CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderDetailForm

    def get_template_names(self):
        if self.request.profile == self.object.seller:
            # return 'order/order_detail_owner.html'
            return 'order/order_detail.html'
        else:
            return 'order/order_detail.html'

    def get_object(self, queryset=None):
        uid = self.kwargs.get('uid', None)
        obj = self.model.objects.get(uid=uid)
        return obj


class OrderPayView(CommonContextMixin, UpdateView):
    model = Order
    form_class = forms.OrderDetailForm
    template_name = 'order/order_detail.html'

    def get_ip(self, **kwargs):
        ''' Reads IP, with alternative way for vestek ? '''
        if self.request.META.get('HTTP_X_FORWARDED_FOR'):
            ip_data = self.request.META.get('HTTP_X_FORWARDED_FOR').split(', ')[0]
            ip = ip_data if ip_data != 'unknown' else None
        else:
            ip = self.request.META.get('REMOTE_ADDR')

        if ip is None:
            return None

        return ip.strip()

    def get_context_data(self, **kwargs):
        context = super(OrderPayView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        context['jsapi'] = self.object.get_jsapi(self.get_ip())
        return context


class OrderProductListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for OrderProduct """
    model = OrderProduct
    template_name_suffix = '_list'  # order/orderproduct_list.html
    permissions = {
        "all": ("order.view_orderproduct",)
    }


class OrderProductDetailView(SellerOwnerOnlyRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for OrderProduct """
    model = OrderProduct
    form_class = forms.OrderProductDetailForm
    template_name = 'adminlte/common_detail_new.html'


class OrderPurchaseView(CarrierInfoRequiredMixin, SellerRequiredMixin, CommonContextMixin, ListView):
    model = Order
    queryset = Order.objects.filter(status=ORDER_STATUS.CREATED, products__is_purchased=False).distinct().order_by(
        '-create_time')
    template_name = 'order/order_purchase.html'
