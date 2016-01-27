VIEWS_HEADER = '''
from django.http import Http404
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework.permissions import AllowAny
from braces.views import MultiplePermissionsRequiredMixin, PermissionRequiredMixin
from apps.adminlte.views import CommonContextMixin
from models import <% ALL_MODELS %>
'''

VIEWS_MODEL_TEMPLATE = '''
# views for <% MODEL_NAME %>

class <% MODEL_NAME %>ListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = <% MODEL_NAME %>
    template_name_suffix = '_list' # <% model_name %>/<% model_name %>_list.html
    permissions = {
        "all": ("<% app_name %>.list_<% model_name %>",)
    }

    def get_context_data(self, **kwargs):
        context = super(<% MODEL_NAME %>ListView, self).get_context_data(**kwargs)
        context['table_titles'] = <% titles %>
        context['table_fields'] = <% fields %>
        return context


class <% MODEL_NAME %>AddView(MultiplePermissionsRequiredMixin, CommonContextMixin, CreateView):
    model = <% MODEL_NAME %>
    # template_name_suffix = '_create'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("<% model_name %>.add_<% model_name %>",)
    }

    def get_context_data(self, **kwargs):
        context = super(<% MODEL_NAME %>AddView, self).get_context_data(**kwargs)
        context['table_titles'] = <% titles %>
        context['table_fields'] = <% fields %>
        return context


class <% MODEL_NAME %>UpdateView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = <% MODEL_NAME %>
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_form.html'
    permissions = {
        "all": ("<% model_name %>.change_<% model_name %>",)
    }
    fields = <% fields %>


class <% MODEL_NAME %>DetailView(MultiplePermissionsRequiredMixin, CommonContextMixin, UpdateView):
    model = <% MODEL_NAME %>
    # template_name_suffix = '_form'
    template_name = 'adminlte/common_detail.html'
    permissions = {
        "all": ("<% model_name %>.view_<% model_name %>",)
    }
    fields = <% fields %>
'''