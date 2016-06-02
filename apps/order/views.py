# coding=utf-8
import datetime
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.forms.models import inlineformset_factory, modelformset_factory
from django_filters import Filter, FilterSet
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from rest_framework import permissions
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.adminlte.views import CommonContextMixin, CommonViewSet
from models import Order, ORDER_STATUS, OrderProduct
from ..member.models import Seller
from ..customer.models import Customer
from ..express.models import ExpressOrder
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
        context = {'form': forms.OrderForm2(),}
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
    template_name = 'order/order_add.html'
    permissions = {
        "all": ("order.add_order",)
    }

    def get_success_url(self):
        if self.object:
            return reverse('order:order-update', args=[self.object.id])
        return reverse('order:order-list-short')

    def get_context_data(self, **kwargs):
        context = super(OrderAddView, self).get_context_data(**kwargs)
        context['new_product_form'] = forms.OrderProductInlineAddForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            url = reverse('order:order-add-detail', args=[form.instance.customer_id])
            return HttpResponseRedirect(url)
        else:
            return self.form_invalid(form)


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
        context['new_product_form'] = forms.OrderProductInlineAddForm()
        context['product_forms'] = forms.OrderProductFormSet(queryset=self.object.products.all())
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        formset = forms.OrderProductFormSet(request.POST)
        for form in formset:
            if form.instance.product or form.instance.name:
                form.fields['order'].initial = self.object.id
                form.base_fields['order'].initial = self.object.id
                form.changed_data.append('order')
                # form.cleaned_data['order'] = self.object
                form.instance.order_id = self.object.id
        instances = formset.save()

        result = super(OrderUpdateView, self).post(request, *args, **kwargs)
        next = request.POST.get('next')
        if next:
            url = reverse('order:order-update', args=[self.object.id])
            return HttpResponseRedirect(url)
        return result


class OrderAddDetailView(OrderUpdateView):
    permissions = {
        "all": ("order.add_order",)
    }

    def get_object(self, queryset=None):
        try:
            object = super(OrderAddDetailView, self).get_object()
        except:

            object = Order(customer_id=self.kwargs['customer_id'])
            object.address_id = self.request.POST['address']
            object.save()
        return object

    def get(self, request, *args, **kwargs):
        customer_id = kwargs['customer_id']
        if not Customer.objects.filter(id=customer_id).exists():
            return HttpResponseRedirect(reverse('order:order-add'))

        self.object = Order(customer_id=customer_id)
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        inlineform_count = int(request.POST['form-TOTAL_FORMS'])
        request.POST._mutable = True
        request.POST['some_data'] = 'test data'
        for i in range(inlineform_count):
            key = 'form-%s-order' % i
            if key in request.POST:
                request.POST[key] = self.object.id
        request.POST._mutable = False

        formset = forms.OrderProductFormSet(request.POST)
        for form in formset:
            if form.instance.product or form.instance.name:
                if 'order' in form._errors:
                    del form._errors['order']
                form.fields['order'].initial = self.object.id
                form.base_fields['order'].initial = self.object.id
                form._changed_data.append('order')
                form.instance.order_id = self.object.id
        instances = formset.save()

        next = request.POST.get('next')
        if next:
            url = reverse('order:order-update', args=[self.object.id])
            return HttpResponseRedirect(url)
        return HttpResponseRedirect(self.get_success_url())


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


class OrderViewSet(CommonViewSet):
    """ api views for Order """
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


class OrderProductViewSet(CommonViewSet):
    """ api views for OrderProduct """
    serializer_class = serializers.OrderProductSerializer
    filter_class = OrderFilter
    permission_classes = [permissions.DjangoModelPermissions]
    search_fields = ['order__customer__name', 'status']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return OrderProduct.objects.all()
        elif self.request.user.is_authenticated():
            return OrderProduct.objects.filter(order__customer__seller=self.request.user)
        else:
            return OrderProduct.objects.none()


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
