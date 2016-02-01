from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from core.adminlte.views import CommonContextMixin, CommonViewSet
import serializers
import forms
from models import Page, Store


# views for Page

class PageListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Page
    template_name_suffix = '_list'  # page/page_list.html
    permissions = {
        "all": ("store.view_page",)
    }

    def get_context_data(self, **kwargs):
        context = super(PageListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Link'] + [u'Name', u'Url', u'Store', u'Price', u'Original Price'] + ['']
        context['table_fields'] = ['link'] + ['title', 'url', 'store', 'price', 'original_price'] + ['id']
        return context


class PageAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Page
    form_class = forms.PageAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("page.add_page",)
    }

    def get_success_url(self):
        return reverse('page-list')


class PageUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Page
    form_class = forms.PageUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("page.change_page",)
    }

    def get_success_url(self):
        return reverse('page-list')


class PageDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Page
    form_class = forms.PageDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("page.view_page",)
    }


# api views for Page

class PageViewSet(CommonViewSet):
    queryset = Page.objects.all()
    serializer_class = serializers.PageSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['title', 'url', 'store', 'price', 'original_price']
    search_fields = ['title', 'url', 'store', 'price', 'original_price']


# views for Store

class StoreListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = Store
    template_name_suffix = '_list'  # store/store_list.html
    permissions = {
        "all": ("store.view_store",)
    }

    def get_context_data(self, **kwargs):
        context = super(StoreListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Link'] + [u'Name', u'Short Name', u'Address', u'Domain', u'Search URL', u'Shipping Rate'] + ['']
        context['table_fields'] = ['link'] + ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate'] + ['id']
        return context


class StoreAddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = Store
    form_class = forms.StoreAddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("store.add_store",)
    }

    def get_success_url(self):
        return reverse('store-list')


class StoreUpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Store
    form_class = forms.StoreUpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("store.change_store",)
    }

    def get_success_url(self):
        return reverse('store-list')


class StoreDetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = Store
    form_class = forms.StoreDetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("store.view_store",)
    }


# api views for Store

class StoreViewSet(CommonViewSet):
    queryset = Store.objects.all()
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']
    search_fields = ['name', 'short_name', 'address', 'domain', 'search_url', 'shipping_rate']

