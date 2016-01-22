import os
import sys
import types
import inspect
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
import serializers
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
    model_list = []


    def handle(self, *args, **options):
        if len(args) < 1:
            self.stderr.write(self.help)
            return
        self.raw_input = args[0]
        self.module_str = args[0] if args[0].find('.models') > 0 else args[0] + '.models'

        try:
            self.import_mod_cls(self.module_str)
            self.get_module_folder()
        except AttributeError as e:
            self.stdout.write("Error: %s" % e)
            return

        self.stdout.write('\n############################## info ##############################')
        self.stdout.write(self.module_str)
        self.stdout.write(str(self.module))
        self.stdout.write(self.app_name)
        # self.stdout.write('%s.%s' % (self.model.__module__, self.model.__name__))
        self.stdout.write(self.module_file)
        self.stdout.write(self.module_path)

        self.stdout.write('\n############################## models ##############################')
        for md in self.model_list:
            self.stdout.write(md.__module__ + '.' + md.__name__)
        return
        self.stdout.write('\n############################## views.py ##############################')
        self.stdout.write(self.get_urls_content())
        self.stdout.write('\n############################## views.py ##############################')
        self.stdout.write(self.get_views_content())

    def import_from_str(self, name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def import_mod_cls(self, name):
        mod = self.import_from_str(name)
        if isinstance(mod, types.ModuleType):
            self.module = mod
            self.import_model(mod)
        elif issubclass(mod, models.Model):
            self.model_list.append(mod)
            self.module = sys.modules[mod.__module__]
        else:
            raise AttributeError('%s is not a model or module' % name)

        if not len(self.model_list):
            raise AttributeError('Found no model in %s' % name)

        self.app_name = self.model_list[0]._meta.app_label

    def import_model(self, mod):
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(self.module_str):
                if issubclass(obj, models.Model):
                    self.model_list.append(obj)


    def get_module_folder(self):
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

    def render_content(self, content):
        return content.replace('<% module_str %>', self.module_str). \
            replace('<% MODEL_NAME %>', self.model.__name__). \
            replace('<% app_name %>', self.app_name). \
            replace('<% model_name %>', self.model.__name__.lower())

    def get_views_content(self):
        return self.render_content(VIEWS_MODULE_TEMPLATE)

    def get_urls_content(self):
        return self.render_content(URLS_MODULE_TEMPLATE)

