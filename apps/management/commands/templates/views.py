VIEWS_HEADER = '''from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from apps.adminlte.views import CommonContextMixin, CommonDeleteView, CommonViewSet
from models import <% ALL_MODELS %>
import serializers
import forms

'''

VIEWS_MODEL_TEMPLATE = '''
# views for <% MODEL_NAME %>

class <% MODEL_NAME %>ListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = <% MODEL_NAME %>
    template_name_suffix = '_list'  # <% model_name %>/<% model_name %>_list.html
    permissions = {
        "all": ("<% app_name %>.list_<% model_name %>",)
    }

    def get_context_data(self, **kwargs):
        context = super(<% MODEL_NAME %>ListView, self).get_context_data(**kwargs)
        context['table_titles'] = ['Link'] + <% titles %> + ['']
        context['table_fields'] = ['link'] + <% fields %> + ['id']
        return context


class <% MODEL_NAME %>AddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = <% MODEL_NAME %>
    # template_name_suffix = '_create'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("<% model_name %>.add_<% model_name %>",)
    }
    success_url = '/<% app_name %>/<% model_name %>/list/'

    def get_context_data(self, **kwargs):
        context = super(<% MODEL_NAME %>AddView, self).get_context_data(**kwargs)
        context.update({'form': forms.<% MODEL_NAME %>AddForm()})
        return context


class <% MODEL_NAME %>UpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = <% MODEL_NAME %>
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("<% model_name %>.change_<% model_name %>",)
    }
    fields = <% fields %>

    def get_context_data(self, **kwargs):
        context = super(<% MODEL_NAME %>UpdateView, self).get_context_data(**kwargs)
        context.update({'form': forms.<% MODEL_NAME %>UpdateForm()})
        return context

    def get_success_url(self):
        return reverse('<% model_name %>-list')


class <% MODEL_NAME %>DetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = <% MODEL_NAME %>
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("<% model_name %>.view_<% model_name %>",)
    }
    fields = <% fields %>

    def get_context_data(self, **kwargs):
        context = super(<% MODEL_NAME %>DetailView, self).get_context_data(**kwargs)
        context.update({'form': forms.<% MODEL_NAME %>DetailForm()})
        return context


# api views for <% MODEL_NAME %>

class <% MODEL_NAME %>ViewSet(CommonViewSet):
    queryset = <% MODEL_NAME %>.objects.all()
    serializer_class = serializers.<% MODEL_NAME %>Serializer
    permission_classes = [permissions.DjangoModelPermissions]
    filter_fields = <% fields %>
    search_fields = <% fields %>


class <% MODEL_NAME %>DeleteView(CommonDeleteView):
    queryset = <% MODEL_NAME %>.objects.all()
    permission_classes = [permissions.DjangoModelPermissions]

'''