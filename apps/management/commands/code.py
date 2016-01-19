import os
import sys
import types
from django.db import models
from optparse import make_option
from django.core.management.base import BaseCommand

VIEWS_MODULE_TEMPLATE = '''
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, DetailView
from <% module_str %> import <% MODEL_NAME %>

class <% MODEL_NAME %>ListView(MultiplePermissionsRequiredMixin, CommonContextMixin, ListView):
    model = <% MODEL_NAME %>
    template_name_suffix = '_list'
    permissions = {
        "all": ("<% app_name %>.view_<% model_name %>",)
    }

    def get_context_data(self, **kwargs):
        context = super(<% MODEL_NAME %>ListView, self).get_context_data(**kwargs)
        return context

'''

VIEWS_MODEL_TEMPLATE = '''

'''

URLS_MODULE_TEMPLATE = '''
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^<% app_name %>/<% model_name %>list/$', views.<% MODEL_NAME %>ListView.as_view(), name='<% model_name %>-list'),
)
'''

URLS_MODEL_TEMPLATE = '''

'''

SERIALIZERS_MODULE_TEMPLATE = '''

'''

SERIALIZERS_MODEL_TEMPLATE = '''

'''


class Command(BaseCommand):
    help = ''' Create code

    Usage: ./manage.py code <module_name>

    Example: ./manage.py code apps.product.models.Product
    '''
    module = None
    model = None


    def handle(self, *args, **options):
        if len(args) < 1:
            self.stderr.write(self.help)
            return
        mod_str = args[0]

        try:
            self.import_mod_cls(mod_str)
            self.get_module_folder()
        except AttributeError as e:
            self.stdout.write("Error: %s" % e)
            return

        self.stdout.write(self.module.__file__)
        self.stdout.write('%s.%s' % (self.model.__module__, self.model.__name__))
        self.stdout.write(self.module_file)
        self.stdout.write(self.module_path)

        self.stdout.write(self.get_views_content())
        self.stdout.write(self.get_views_content())


    def import_mod_cls(self, name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)

        if issubclass(mod, models.Model):
            self.model = mod
            self.module = sys.modules[mod.__module__]
        elif isinstance(mod, types.ModuleType):
            self.module = mod
            raise AttributeError('%s is not a model' % name)
        else:
            raise AttributeError('%s is not a model' % name)
        self.module_str = name
        self.app_name = self.model._meta.app_label

    def get_module_folder(self):
        if self.model:
            self.module_file = sys.modules[self.model.__module__].__file__[:-1]
            self.module_path = os.path.dirname(sys.modules[self.model.__module__].__file__)
        elif self.module:
            self.module_file = self.module.__file__[:-1]
            self.module_path = os.path.dirname(self.module.__file__)

    @property
    def get_views_file(self):
        return os.path.join(self.module_path, 'views.py')

    @property
    def get_urls_file(self):
        return os.path.join(self.module_path, 'urls.py')

    @property
    def get_serializers_file(self):
        return os.path.join(self.module_path, 'serializers.py')

    def create_file(self, file_path, content):
        with open(file_path, 'a') as f:
            f.write('content')

    def append_file(self, file_path, content):
        with open(file_path, 'w+') as f:
            f.write('content')

    def render_content(self,content):
        return content.replace('<% module_str %>', self.module_str). \
            replace('<% MODEL_NAME %>', self.model.__name__). \
            replace('<% app_name %>', self.app_name). \
            replace('<% model_name %>', self.model.__name__.lower())

    def get_views_content(self):
        return self.render_content(VIEWS_MODULE_TEMPLATE)

    def get_urls_content(self):
        return self.render_content(URLS_MODULE_TEMPLATE)




