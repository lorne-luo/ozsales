# coding=utf-8
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.db import transaction
from django.core.exceptions import ValidationError, SuspiciousOperation
from django.forms.models import inlineformset_factory, modelformset_factory
from django.views.generic.edit import BaseUpdateView, ProcessFormView
from rest_framework.decorators import list_route
from django_filters import FilterSet
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin, GroupRequiredMixin

from core.auth_user.constant import MEMBER_GROUP, FREE_MEMBER_GROUP, ADMIN_GROUP
from core.views.views import CommonContextMixin, CommonViewSet
from models import Order, ORDER_STATUS, OrderProduct
from ..member.models import Seller
from ..customer.models import Customer
from ..express.forms import ExpressOrderInlineAddForm, ExpressOrderFormSet
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


class OrderListView(GroupRequiredMixin, CommonContextMixin, ListView):
    model = Order
    template_name_suffix = '_list'  # order/order_list.html
    group_required = [MEMBER_GROUP, FREE_MEMBER_GROUP]


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


class OrderAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Order
    form_class = forms.OrderAddForm
    # template_name = 'adminlte/common_form.html'
    template_name = 'order/order_add.html'
    permissions = {
        "all": ("order.add_order",)
    }

    def get_success_url(self):
        if '_continue' in self.request.POST and self.object:
            return reverse('order:order-update', args=[self.object.id])
        else:
            return reverse('order:order-list-short')

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
    permissions = {"all": ["order.change_order"]}
    products_prefix = 'products'
    express_orders_prefix = 'express_orders'

    def get_success_url(self):
        if '_continue' in self.request.POST and self.object:
            return reverse('order:order-update', args=[self.object.id])
        else:
            return reverse('order:order-list-short')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        instance = getattr(self, 'object')

        context['new_product_template'] = forms.OrderProductInlineAddForm(prefix='%s_template' % self.products_prefix,
                                                                          initial={'order': instance})
        context['new_express_template'] = ExpressOrderInlineAddForm(prefix='%s_template' % self.express_orders_prefix,
                                                                    initial={'order': instance})

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

    def save_product_formset(self, request):
        products_formset = forms.OrderProductFormSet(request.POST, request.FILES, prefix=self.products_prefix,
                                                     instance=self.object)
        for form in products_formset:
            form.is_valid()
            if form.instance.product_id or form.instance.name:
                form.fields['order'].initial = self.object.id
                form.base_fields['order'].initial = self.object.id
                form.changed_data.append('order')
                form.instance.order_id = self.object.id
                form.instance.order = self.object
            else:
                form._changed_data = []
            if form._errors and 'order' in form._errors:
                del form._errors['order']

        if not products_formset.is_valid():
            raise SuspiciousOperation(str(products_formset.errors))
        products_formset.save()

    def save_express_formset(self, request):
        express_formset = ExpressOrderFormSet(request.POST, request.FILES, prefix=self.express_orders_prefix,
                                              instance=self.object)
        for form in express_formset:
            form.is_valid()
            if form.instance.track_id:
                form.fields['order'].initial = self.object.id
                form.base_fields['order'].initial = self.object.id
                form.changed_data.append('order')
                form.instance.order_id = self.object.id
                form.instance.order = self.object
            else:
                form._changed_data = []
            if form._errors and 'order' in form._errors:
                del form._errors['order']

        if not express_formset.is_valid():
            raise SuspiciousOperation(str(express_formset.errors))
        express_formset.save()

    @transaction.atomic
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
    permissions = {
        "all": ("order.add_order",)
    }

    def get_object(self, queryset=None):
        try:
            object = super(OrderAddDetailView, self).get_object()
        except:
            object = Order(customer_id=self.kwargs['customer_id'])
            object.address_id = self.request.POST['address']
            object.seller = self.request.user.profile
            object.save()
        return object

    def get(self, request, *args, **kwargs):
        customer_id = kwargs['customer_id']
        if not Customer.objects.filter(id=customer_id).exists():
            return HttpResponseRedirect(reverse('order:order-add'))

        self.object = Order(customer_id=customer_id)
        form = self.get_form()
        return self.render_to_response(self.get_context_data(form=form))

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # fill express_orders-%s-order field
        products_formset_count = int(request.POST['products-TOTAL_FORMS'])
        express_formset_count = int(request.POST['express_orders-TOTAL_FORMS'])
        request.POST._mutable = True
        for i in range(products_formset_count):
            key = 'products-%s-order' % i
            product_key = 'products-%s-product' % i
            name_key = 'products-%s-name' % i
            if request.POST[product_key] or request.POST[name_key]:
                request.POST[key] = self.object.id

        for i in range(express_formset_count):
            key = 'express_orders-%s-order' % i
            track_key = 'express_orders-%s-track_id' % i
            if request.POST[track_key]:
                request.POST[key] = self.object.id
        request.POST._mutable = False

        # order products
        self.save_product_formset(request)

        # express orders
        self.save_express_formset(request)

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
        from ..weixin.models import WxApp
        context = super(OrderPayView, self).get_context_data(**kwargs)
        self.object = self.get_object()
        context['jsapi'] = self.object.get_jsapi(self.get_ip())
        return context


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['in', 'exact'],
            'customer__name': ['exact', 'contains']
        }


class NewOrderFilter(FilterSet):
    class Meta:
        model = Order
        exclude = []

    @property
    def qs(self):
        qs = super(NewOrderFilter, self).qs.filter(Q(status=ORDER_STATUS.CREATED) | Q(is_paid=False))
        return qs


class OrderViewSet(GroupRequiredMixin, CommonViewSet):
    """ api views for Order """
    serializer_class = serializers.OrderSerializer
    filter_class = OrderFilter
    filter_fields = ['id']
    search_fields = ['customer__name', 'address__name', 'address__address']
    group_required = [ADMIN_GROUP, MEMBER_GROUP, FREE_MEMBER_GROUP]

    def get_queryset(self):
        return Order.objects.filter(seller=self.request.user.profile).select_related('address', 'customer')

    @list_route(methods=['post', 'get'])
    def new(self, request, *args, **kwargs):
        self.filter_class = NewOrderFilter
        return super(OrderViewSet, self).list(self, request, *args, **kwargs)


class OrderProductListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for OrderProduct """
    model = OrderProduct
    template_name_suffix = '_list'  # order/orderproduct_list.html
    permissions = {
        "all": ("order.view_orderproduct",)
    }


class OrderProductDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for OrderProduct """
    model = OrderProduct
    form_class = forms.OrderProductDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("order.view_orderproduct",)
    }


class OrderProductViewSet(CommonViewSet):
    """ api views for OrderProduct """
    serializer_class = serializers.OrderProductSerializer
    filter_fields = ['id']
    search_fields = ['order__customer__name', 'order__address__name', 'name', 'product__name_en', 'product__name_cn',
                     'product__brand__name_en', 'product__brand__name_cn']

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = OrderProduct.objects.all()
        elif self.request.user.is_authenticated():
            queryset = OrderProduct.objects.filter(order__customer__seller=self.request.user)
        else:
            queryset = OrderProduct.objects.none()

        return queryset.select_related('order', 'product')
