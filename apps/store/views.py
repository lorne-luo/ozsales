# coding=utf-8
from braces.views import MultiplePermissionsRequiredMixin, SuperuserRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView

from core.django.views import CommonContextMixin
from .models import Page, Store
from . import forms


# views for Page

class PageListView(SuperuserRequiredMixin, CommonContextMixin, ListView):
    model = Page
    template_name_suffix = '_list'  # store/page_list.html


class PageAddView(SuperuserRequiredMixin, CommonContextMixin, CreateView):
    model = Page
    form_class = forms.PageAddForm
    template_name = 'adminlte/common_form.html'


class PageUpdateView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = Page
    form_class = forms.PageUpdateForm
    template_name = 'adminlte/common_form.html'


class PageDetailView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = Page
    form_class = forms.PageDetailForm
    template_name = 'adminlte/common_detail_new.html'


# views for Store

class StoreListView(SuperuserRequiredMixin, CommonContextMixin, ListView):
    model = Store
    template_name_suffix = '_list'  # store/store_list.html


class StoreAddView(SuperuserRequiredMixin, CommonContextMixin, CreateView):
    model = Store
    form_class = forms.StoreAddForm
    template_name = 'adminlte/common_form.html'


class StoreUpdateView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = Store
    form_class = forms.StoreUpdateForm
    template_name = 'adminlte/common_form.html'


class StoreDetailView(SuperuserRequiredMixin, CommonContextMixin, UpdateView):
    model = Store
    form_class = forms.StoreDetailForm
    template_name = 'adminlte/common_detail_new.html'
