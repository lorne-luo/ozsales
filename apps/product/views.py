from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework import permissions
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from core.adminlte.views import CommonContextMixin, CommonViewSet
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
        context = {'form': forms.ProductForm(), }
        if pk:
            product = get_object_or_404(Product, id=pk)
            context['product'] = product

        return self.render_to_response(context)


class ProductListView(CommonContextMixin, ListView):
    model = Product
    # template_name_suffix = '_list'
    # template_name = 'product_list.html'
    # permissions = {
    #     "all": ("product.view_product",)
    # }

    def get_template_names(self):
        if not self.request.user.is_authenticated():
            return ['product/allowany_product_list.html']
        return super(ProductListView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Pic', 'Name', 'Brand', 'Normal Price', 'Bargain Price', 'Sell Price', '']
        context['table_fields'] = ['pic', 'link', 'brand', 'normal_price', 'bargain_price', 'safe_sell_price', 'id']
        context['brands'] = Brand.objects.all()
        return context


class ProductAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Product
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
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("product.change_product",)
    }
    fields = ['name_en', 'name_cn', 'pic', 'brand', 'spec1', 'category', 'normal_price', 'bargain_price',
              'safe_sell_price']


class ProductDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Product
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_detail.html'
    permissions = {
        "all": ("product.view_product",)
    }
    fields = ['name_en', 'name_cn', 'pic', 'brand', 'spec1', 'category', 'normal_price', 'bargain_price',
              'safe_sell_price']


class PublicListAPIView(CommonListCreateAPIView):
    ''' Public API view for Product '''
    model = Product
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return Http404


class ProductViewSet(CommonViewSet):
    """
     A viewset for viewing and editing  instances.
    """
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['Pic', 'Name', 'Brand', 'Normal Price', 'Bargain Price', 'Sell Price', '']
    search_fields = ['pic', 'link', 'brand', 'normal_price', 'bargain_price', 'safe_sell_price', 'id']


class BrandListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Brand
    template_name_suffix = '_list'  # product/brand_list.html
    permissions = {
        "all": ("product.view_brand",)
    }

    def get_context_data(self, **kwargs):
        context = super(BrandListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Link'] + ['Name_En', 'Name_Cn', 'Country', 'Remarks'] + ['']
        context['table_fields'] = ['link'] + ['name_en', 'name_cn', 'country', 'remarks'] + ['id']
        return context


class BrandAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Brand
    form_class = forms.BrandAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("brand.add_brand",)
    }

    def get_success_url(self):
        return reverse('product:brand-list')


class BrandUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Brand
    form_class = forms.BrandUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("brand.change_brand",)
    }

    def get_success_url(self):
        return reverse('product:brand-list')


class BrandDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Brand
    form_class = forms.BrandDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("brand.view_brand",)
    }


# api views for Brand

class BrandViewSet(CommonViewSet):
    queryset = Brand.objects.all()
    serializer_class = serializers.BrandSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['name_en', 'name_cn', 'country', 'remarks']
    search_fields = ['name_en', 'name_cn', 'country', 'remarks']

