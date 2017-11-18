from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView
from dal import autocomplete
from rest_framework import permissions
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.views.views import CommonContextMixin, CommonViewSet
from core.api.views import CommonListCreateAPIView
from models import Product, Brand
import serializers
import forms


class ProductList(MultiplePermissionsRequiredMixin, TemplateView):
    ''' List of products. '''
    template_name = 'product/product-list.html'
    permissions = {
        "any": ("product.add_product", "product.view_product")
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return self.render_to_response(context)


class ProductAddEdit(MultiplePermissionsRequiredMixin, TemplateView):
    ''' Add/Edit a product. '''
    template_name = 'product/product-edit.html'
    permissions = {
        "any": ("product.add_product", "product.view_product")
    }

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', '')
        context = {'form': forms.ProductForm()}
        if pk:
            product = get_object_or_404(Product, id=pk)
            context['product'] = product

        return self.render_to_response(context)


class ProductListView(CommonContextMixin, ListView):
    model = Product

    # template_name_suffix = '_list'
    # template_name = 'product_list.html'

    def get_template_names(self):
        if not self.request.user.is_authenticated():
            return ['product/allowany_product_list.html']
        return super(ProductListView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['table_titles'] = ['Pic', 'Name', 'Brand', 'Normal Price', 'Bargain Price', 'Sell Price', '']
            context['table_fields'] = ['pic', 'link', 'brand', 'normal_price', 'bargain_price', 'safe_sell_price', 'id']
        else:
            context['table_titles'] = ['Pic', 'Name', 'Brand', 'Sell Price']
            context['table_fields'] = ['pic', 'link', 'brand', 'safe_sell_price']
        context['brands'] = Brand.objects.all()
        return context


class ProductAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Product
    form_class = forms.ProductAddForm
    # template_name_suffix = '_create'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("product.add_product",)
    }

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Pic', 'Name', 'Brand', 'Normal Price', 'Bargain Price', 'Sell Price', '']
        context['table_fields'] = ['pic', 'link', 'brand', 'normal_price', 'bargain_price', 'safe_sell_price', 'id']
        return context


class ProductUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Product
    form_class = forms.ProductAddForm
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("product.change_product",)
    }


class ProductDetailView(CommonContextMixin, UpdateView):
    model = Product
    # template_name_suffix = '_form'
    fields = ['name_en', 'name_cn', 'pic', 'brand', 'category', 'safe_sell_price']


class ProductViewSet(CommonViewSet):
    """
     A viewset for viewing and editing  instances.
    """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_fields = ['name_en', 'name_cn', 'brand__id', 'brand__name_cn', 'brand__name_en']
    search_fields = ['name_en', 'name_cn', 'brand__name_cn', 'brand__name_en']


class BrandListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for Brand """
    model = Brand
    template_name_suffix = '_list'  # product/brand_list.html
    permissions = {
        "all": ("product.view_brand",)
    }


class BrandAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for Brand """
    model = Brand
    form_class = forms.BrandAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("product.add_brand",)
    }


class BrandUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for Brand """
    model = Brand
    form_class = forms.BrandUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("product.change_brand",)
    }


class BrandDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for Brand """
    model = Brand
    form_class = forms.BrandDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("product.view_brand",)
    }


class BrandViewSet(CommonViewSet):
    """ API views for Brand """
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    filter_fields = ['name_en', 'name_cn']
    search_fields = ['name_en', 'name_cn']


class ProductAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.all().order_by('brand__name_en', 'name_cn')

        if self.q:
            qs = qs.filter(Q(name_cn__icontains=self.q) | Q(name_en__icontains=self.q) |
                           Q(brand__name_en__icontains=self.q) | Q(brand__name_cn__icontains=self.q))
        return qs
