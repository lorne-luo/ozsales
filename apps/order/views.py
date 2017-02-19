# coding=utf-8
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError
from django.forms.models import inlineformset_factory, modelformset_factory
from django_filters import FilterSet
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
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
    permissions = {
        "all": ("order.change_order",)
    }

    def get_success_url(self):
        if '_continue' in self.request.POST and self.object:
            return reverse('order:order-update', args=[self.object.id])
        else:
            return reverse('order:order-list-short')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)

        context['new_product_form'] = forms.OrderProductInlineAddForm(prefix='products')
        product_forms = forms.OrderProductFormSet(queryset=self.object.products.all(), prefix='products')
        context['product_forms'] = product_forms

        context['new_express_form'] = ExpressOrderInlineAddForm(prefix='express_orders')
        express_forms = ExpressOrderFormSet(queryset=self.object.express_orders.all(), prefix='express_orders')
        context['express_forms'] = express_forms

        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # order products
        products_formset = forms.OrderProductFormSet(request.POST, request.FILES, prefix='products')
        for form in products_formset:
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
            form.is_valid()

        if not products_formset.is_valid():
            return HttpResponse(str(products_formset.errors))
        products_formset.save()

        # express orders
        express_formset = ExpressOrderFormSet(request.POST, request.FILES, prefix='express_orders')
        for form in express_formset:
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
            form.is_valid()

        if not express_formset.is_valid():
            return HttpResponse(str(express_formset.errors))
        express_formset.save()

        return super(OrderUpdateView, self).post(request, *args, **kwargs)


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

        products_formset = forms.OrderProductFormSet(request.POST, request.FILES, prefix='products')
        for form in products_formset:
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

            form.is_valid()

        if not products_formset.is_valid():
            return HttpResponse(str(products_formset.errors))
        products_formset.save()

        express_formset = ExpressOrderFormSet(request.POST, request.FILES, prefix='express_orders')
        for form in express_formset:
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

            form.is_valid()

        if not express_formset.is_valid():
            return HttpResponse(str(express_formset.errors))
        express_formset.save()

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


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            'status': ['in', 'exact'],
            'customer__name': ['exact', 'contains']
        }


class OrderViewSet(CommonViewSet):
    """ api views for Order """
    serializer_class = serializers.OrderSerializer
    filter_class = OrderFilter
    filter_fields = ['id']
    search_fields = ['customer__name', 'address__name', 'address__address']

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Order.objects.all()
        elif self.request.user.is_authenticated():
            queryset = Order.objects.filter(customer__seller=self.request.user)
        else:
            queryset = Order.objects.none()

        return queryset.select_related('address', 'customer')


class OrderProductListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for OrderProduct """
    model = OrderProduct
    template_name_suffix = '_list'  # order/orderproduct_list.html
    permissions = {
        "all": ("order.view_orderproduct",)
    }


# class OrderProductAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
#     """ Add views for OrderProduct """
#     model = OrderProduct
#     form_class = forms.OrderProductAddForm
#     template_name = 'adminlte/common_form.html'
#     permissions = {
#         "all": ("orderproduct.add_orderproduct",)
#     }
#
#
# class OrderProductUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
#     """ Update views for OrderProduct """
#     model = OrderProduct
#     form_class = forms.OrderProductUpdateForm
#     template_name = 'adminlte/common_form.html'
#     permissions = {
#         "all": ("orderproduct.change_orderproduct",)
#     }


class OrderProductDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for OrderProduct """
    model = OrderProduct
    form_class = forms.OrderProductDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("orderproduct.view_orderproduct",)
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
