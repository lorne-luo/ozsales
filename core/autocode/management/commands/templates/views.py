VIEWS_HEADER = '''# coding=utf-8
from django.views.generic import ListView, CreateView, UpdateView
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from core.views.views import CommonContextMixin, CommonViewSet
from models import <% ALL_MODELS %>
import serializers
import forms

'''

VIEWS_MODEL_TEMPLATE = '''
class <% MODEL_NAME %>ListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    """ List views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    template_name_suffix = '_list'  # <% app_name %>/<% model_name %>_list.html
    permissions = {
        "all": ("<% app_name %>.view_<% model_name %>",)
    }


class <% MODEL_NAME %>AddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    """ Add views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    form_class = forms.<% MODEL_NAME %>AddForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("<% model_name %>.add_<% model_name %>",)
    }


class <% MODEL_NAME %>UpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Update views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    form_class = forms.<% MODEL_NAME %>UpdateForm
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("<% model_name %>.change_<% model_name %>",)
    }


class <% MODEL_NAME %>DetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    """ Detail views for <% MODEL_NAME %> """
    model = <% MODEL_NAME %>
    form_class = forms.<% MODEL_NAME %>DetailForm
    template_name = 'adminlte/common_detail_new.html'
    permissions = {
        "all": ("<% model_name %>.view_<% model_name %>",)
    }


class <% MODEL_NAME %>ViewSet(CommonViewSet):
    """ API views for <% MODEL_NAME %> """
    queryset = <% MODEL_NAME %>.objects.all()
    serializer_class = serializers.<% MODEL_NAME %>Serializer
    filter_fields = ['id'] + <% fields %>
    search_fields = <% fields %>

'''