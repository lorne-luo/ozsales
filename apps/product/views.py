from django.db.models import Q
from django.views.generic import ListView, CreateView, UpdateView
from dal import autocomplete
from rest_framework import permissions
from braces.views import MultiplePermissionsRequiredMixin

from core.views.autocomplete import HansSelect2ViewMixin
from core.libs.string import include_non_asc
from core.views.permission import ProfileRequiredMixin
from core.views.views import CommonContextMixin, CommonViewSet
from models import Product, Brand
import serializers
import forms


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


class ProductAutocomplete(ProfileRequiredMixin, HansSelect2ViewMixin, autocomplete.Select2QuerySetView):
    model = Product
    paginate_by = 20
    create_field = 'name_cn'
    profile_required = ('member.seller',)

    def create_object(self, text):
        return self.get_queryset().create(**{self.create_field: text, 'seller': self.request.profile})

    def get_queryset(self):
        qs = Product.objects.all_for_seller(self.request.user).order_by('brand__name_en', 'name_cn')

        if include_non_asc(self.q):
            qs = qs.filter(Q(name_cn__icontains=self.q) | Q(brand__name_cn__icontains=self.q))
        else:
            # all ascii, number and letter
            key = self.q.lower()
            qs = qs.filter(
                Q(pinyin__contains=key) | Q(name_en__icontains=key) | Q(brand__name_en__icontains=key))
        return qs
