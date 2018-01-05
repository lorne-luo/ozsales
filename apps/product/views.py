from django.views.generic import ListView, CreateView, UpdateView
from braces.views import MultiplePermissionsRequiredMixin

from core.django.views import CommonContextMixin
from .models import Product, Brand
from . import forms


class ProductListView(CommonContextMixin, ListView):
    model = Product
    template_name_suffix = '_list'

    def get_template_names(self):
        if not self.request.user.is_authenticated():
            return ['product/allowany_product_list.html']
        return super(ProductListView, self).get_template_names()

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['table_titles'] = ['Pic', 'Name', 'Brand', 'Last Price', 'Avg Price', '']
            context['table_fields'] = ['pic', 'link', 'brand', 'last_sell_price', 'avg_sell_price', 'id']
        else:
            context['table_titles'] = ['Pic', 'Name', 'Brand', 'Avg Price']
            context['table_fields'] = ['pic', 'link', 'brand', 'avg_sell_price']
        context['brands'] = Brand.objects.all()
        return context


class ProductAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Product
    form_class = forms.ProductAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("product.add_product",)
    }

    def get_context_data(self, **kwargs):
        context = super(ProductAddView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Pic', 'Name', 'Brand', '']
        context['table_fields'] = ['pic', 'link', 'brand', 'id']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.seller = self.request.profile
        return super(ProductAddView, self).form_valid(form)


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
    fields = ['name_en', 'name_cn', 'pic', 'brand', 'avg_sell_price']


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
