from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework_extensions.mixins import PaginateByMaxMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, permissions
from apps.adminlte.views import CommonContextMixin
from models import Page, Store
import serializers


# views for Page

class PageListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Page
    template_name_suffix = '_list'  # page/page_list.html
    permissions = {
        "all": ("store.list_page",)
    }

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Link'] + [u'name', u'url', u'Store', u'price', u'original price'] + ['']
        context['table_fields'] = ['link'] + ['title', 'url', 'store', 'price', 'original_price'] + ['id']
        return context


class PageAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Page
    # template_name_suffix = '_create'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("page.add_page",)
    }
    success_url = '/store/page/list/'

    def get_context_data(self, **kwargs):
        context = super(PageAddView, self).get_context_data(**kwargs)
        context['table_titles'] = [u'name', u'url', u'Store', u'price', u'original price']
        context['table_fields'] = ['title', 'url', 'store', 'price', 'original_price']
        return context


class PageUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Page
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("page.change_page",)
    }
    fields = ['title', 'url', 'store', 'price', 'original_price']


class PageDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Page
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("page.view_page",)
    }
    fields = ['title', 'url', 'store', 'price', 'original_price']


# api views for Page

class PageViewSet(PaginateByMaxMixin, ModelViewSet):
    filter_backends = (filters.SearchFilter,
                       filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    max_paginate_by = 200
    serializer_class = serializers.PageSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Page.objects.all()
    filter_fields = ['title', 'url', 'store', 'price', 'original_price']
    search_fields = ['title', 'url', 'store', 'price', 'original_price']

# views for Store

class StoreListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Store
    template_name_suffix = '_list'  # store/store_list.html
    permissions = {
        "all": ("store.list_store",)
    }

    def get_context_data(self, **kwargs):
        context = super(StoreListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Link'] + [u'name', u'short name', u'address', u'domain', u'Search URL', u'Shipping Rate'] + ['']
        context['table_fields'] = ['link'] + ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate'] + ['id']
        return context


class StoreAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Store
    # template_name_suffix = '_create'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("store.add_store",)
    }
    success_url = '/store/store/list/'

    def get_context_data(self, **kwargs):
        context = super(StoreAddView, self).get_context_data(**kwargs)
        context['table_titles'] = [u'name', u'short name', u'address', u'domain', u'Search URL', u'Shipping Rate']
        context['table_fields'] = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']
        return context


class StoreUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Store
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("store.change_store",)
    }
    fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


class StoreDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Store
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("store.view_store",)
    }
    fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']


# api views for Store

class StoreViewSet(PaginateByMaxMixin, ModelViewSet):
    filter_backends = (filters.SearchFilter,
                       filters.DjangoFilterBackend,
                       filters.OrderingFilter)
    max_paginate_by = 200
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    queryset = Store.objects.all()
    filter_fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']
    search_fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']
