import os
import sys
import types
import inspect
import shutil
from django.db import models
from optparse import make_option
from django.core.management.base import BaseCommand
from templates.views import VIEWS_HEADER, VIEWS_MODEL_TEMPLATE
from templates.urls import URLS_HEADER, URLS_MODEL_TEMPLATE
from templates.serializers import SERIALIZERS_HEADER, SERIALIZERS_MODEL_TEMPLATE
from templates.templates import LIST_JS, LIST_TEMPLATES


class Command(BaseCommand):
    help = ''' Create code

    Usage: ./manage.py code <module_name>

    Example: ./manage.py code apps.product.models.Product
    '''
    module = None
    model_list = []
    fields = []
    titles = []


    def handle(self, *args, **options):
        if len(args) < 1:
            self.stderr.write(self.help)
            return
        self.raw_input = args[0]
        self.module_str = args[0] if args[0].find('.models') > 0 else args[0] + '.models'

        try:
            self.scan_models(self.module_str)
        except AttributeError as e:
            self.stdout.write("Error: %s" % e)
            return

        self.get_model_context(self.model_list[0])

        self.stdout.write('\n############################## info ##############################')
        self.stdout.write(self.module_str)
        self.stdout.write(str(self.module))
        self.stdout.write(self.app_name)
        # self.stdout.write('%s.%s' % (self.model.__module__, self.model.__name__))
        self.stdout.write(self.module_file)
        self.stdout.write(self.module_folder)
        self.stdout.write(self.js_folder)
        self.stdout.write(self.templates_folder)
        self.stdout.write(self.urls_file)

        self.stdout.write('\n############################## models ##############################')
        for md in self.model_list:
            self.stdout.write(md.__module__ + '.' + md.__name__)

        # self.stdout.write('\n############################## urls.py ##############################')
        # self.stdout.write(self.get_urls_content())
        # self.stdout.write('\n############################## views.py ##############################')
        # self.stdout.write(self.get_views_content())
        # self.stdout.write('\n############################## serializers.py ##############################')
        # self.stdout.write(self.get_serializers_content())
        self.run()

    def import_module(self, name):
        components = name.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod

    def scan_models(self, name):
        mod = self.import_module(name)
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
        self.module_file = self.module.__file__[:-1]
        self.module_folder = os.path.dirname(self.module.__file__)
        self.serializers_file = os.path.join(self.module_folder, 'serializers.py')
        self.views_file = os.path.join(self.module_folder, 'views.py')
        self.urls_file = os.path.join(self.module_folder, 'urls.py')
        self.js_folder = os.path.join(self.module_folder, 'static', 'js', self.app_name)
        self.templates_folder = os.path.join(self.module_folder, 'templates', self.app_name)

    def get_fields_and_titles(self, model):
        return [mf.name for mf in model._meta.fields], [unicode(mf.verbose_name) for mf in model._meta.fields]

    def import_model(self, mod):
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(self.module_str):
                if issubclass(obj, models.Model):
                    self.model_list.append(obj)

    def create_base_folder(self, path):
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def create_file(self, file_path, content):
        with open(file_path, 'w+') as f:
            f.write(content)

    def append_file(self, file_path, content):
        with open(file_path, 'w+') as f:
            f.write(content)

    def get_model_context(self, model):
        fields_name = [mf.name for mf in model._meta.fields]
        fields_title = [unicode(mf.verbose_name) for mf in model._meta.fields]

        print fields_name
        print fields_title

    # ============= generate content ==============
    def render_content(self, content, model):
        fields, titles = self.get_fields_and_titles(model)
        all_models = ', '.join([md.__name__ for md in self.model_list])

        return content.replace('<% module_str %>', self.module_str). \
            replace('<% app_name %>', self.app_name). \
            replace('<% MODEL_NAME %>', model.__name__). \
            replace('<% model_name %>', model.__name__.lower()). \
            replace('<% fields %>', str(fields)). \
            replace('<% titles %>', str(titles)). \
            replace('<% ALL_MODELS %>', all_models)

    def get_urls_content(self):
        content = URLS_HEADER
        for model in self.model_list:
            content += self.render_content(URLS_MODEL_TEMPLATE, model)
        self.stdout.write(content)
        return content

    def get_views_content(self):
        content = self.render_content(VIEWS_HEADER, self.model_list[0])
        for model in self.model_list:
            content += self.render_content(VIEWS_MODEL_TEMPLATE, model)
        self.stdout.write(content)
        return content

    def get_serializers_content(self):
        content = SERIALIZERS_HEADER
        for model in self.model_list:
            content += self.render_content(SERIALIZERS_MODEL_TEMPLATE, model)
        self.stdout.write(content)
        return content

    def run(self):
        self.stdout.write('\n######### %s #########' % self.urls_file)
        self.create_file(self.urls_file, self.get_urls_content())
        self.stdout.write('\n######### %s #########' % self.views_file)
        self.create_file(self.views_file, self.get_views_content())
        self.stdout.write('\n######### %s #########' % self.serializers_file)
        self.create_file(self.serializers_file, self.get_serializers_content())

        for model in self.model_list:
            list_js_file = '%s/static/js/%s/%s_list.js' % (self.module_folder, self.app_name, model.__name__.lower())
            self.create_base_folder(list_js_file)
            self.stdout.write('\n######### %s #########' % list_js_file)
            content = self.render_content(LIST_JS, model)
            self.stdout.write(content)
            self.create_file(list_js_file, content)

            list_template_file = '%s/templates/%s/%s_list.html' % (
                self.module_folder, self.app_name, model.__name__.lower())
            self.create_base_folder(list_template_file)
            self.stdout.write('\n######### %s #########' % list_template_file)
            content = self.render_content(LIST_TEMPLATES, model)
            self.stdout.write(content)
            self.create_file(list_template_file, content)

