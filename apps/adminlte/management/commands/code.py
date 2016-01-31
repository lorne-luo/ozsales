import os
import sys
import types
import inspect
import shutil
from django.db import models
from optparse import make_option
from django.core import management
from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option

from templates.urls import URLS_HEADER, URLS_MODEL_TEMPLATE, URLS_FOOTER
from templates.views import VIEWS_HEADER, VIEWS_MODEL_TEMPLATE
from templates.forms import FORMS_HEADER, FORMS_MODEL_TEMPLATE
from templates.serializers import SERIALIZERS_HEADER, SERIALIZERS_MODEL_TEMPLATE
from templates.templates import LIST_JS, LIST_TEMPLATES


class Command(BaseCommand):
    help = ''' Create code

    Usage: ./manage.py code [--overwrite] <module_name>

    Example:

        ./manage.py code apps.product

        ./manage.py code -o apps.product.models.Product

        ./manage.py code apps/product/

    '''

    option_list = BaseCommand.option_list + (
        make_option("--overwrite", "-o", action="store_true", dest="is_overwrite", default=False,
                    help="Overwrite all files."),
    )

    args = "app folder path or models.py path"
    module = None
    model_list = []
    is_overwrite = False

    def handle(self, *args, **options):
        if len(args) < 1:
            self.stderr.write(self.help)
            return
        self.is_overwrite = options.get("is_overwrite")

        self.raw_input = args[0]
        self.module_str = args[0].replace('.py', '').replace('/', '.').strip('.')
        self.module_str = self.module_str if '.models' in self.module_str else self.module_str + '.models'

        try:
            self.scan_models(self.module_str)
        except AttributeError as e:
            self.stdout.write("Error: %s" % e)
            return

        self.stdout.write('\n############################## info ##############################')
        self.stdout.write(self.module_str)
        self.stdout.write(self.app_str)
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
        self.app_str = self.module_str.replace('.models', '')
        self.module_file = self.module.__file__[:-1]
        self.module_folder = os.path.dirname(self.module.__file__)
        self.serializers_file = os.path.join(self.module_folder, 'serializers.py')
        self.views_file = os.path.join(self.module_folder, 'views.py')
        self.urls_file = os.path.join(self.module_folder, 'urls.py')
        self.forms_file = os.path.join(self.module_folder, 'forms.py')
        self.js_folder = os.path.join(self.module_folder, 'static', 'js', self.app_name, '%s_list.js')
        self.templates_folder = os.path.join(self.module_folder, 'templates', self.app_name, '%s_list.html')
        self.all_models_str = ', '.join([md.__name__ for md in self.model_list])

    def get_fields_and_titles(self, model):
        titles = []
        fields = []
        for mf in model._meta.fields:
            if mf.name == 'id':
                continue
            fields.append(mf.name)
            title = unicode(mf.verbose_name)
            if title and title[0].islower():
                title = title.title()
            titles.append(title)

        return fields, titles

    def import_model(self, mod):
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            if obj.__module__.startswith(self.module_str):
                if issubclass(obj, models.Model):
                    self.model_list.append(obj)

    def make_folder(self, path):
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def create_file(self, file_path, content):
        if os.path.isfile(file_path) and not self.is_overwrite:
            file_path += '.code'
        with open(file_path, 'w+') as f:
            f.write(content)

    def append_file(self, file_path, content):
        with open(file_path, 'w+') as f:
            f.write(content)

    # ============= generate content ==============
    def render_content(self, content, model):
        fields, titles = self.get_fields_and_titles(model)

        return content.replace('<% module_str %>', self.module_str). \
            replace('<% app_name %>', self.app_name). \
            replace('<% MODEL_NAME %>', model.__name__). \
            replace('<% model_name %>', model.__name__.lower()). \
            replace('<% fields %>', str(fields)). \
            replace('<% titles %>', str(titles)). \
            replace('<% ALL_MODELS %>', self.all_models_str)

    def get_urls_content(self):
        content = URLS_HEADER
        for model in self.model_list:
            content += self.render_content(URLS_MODEL_TEMPLATE, model)
        content += URLS_FOOTER
        self.stdout.write(content)
        return content

    def get_views_content(self):
        content = VIEWS_HEADER.replace('<% ALL_MODELS %>', self.all_models_str)
        for model in self.model_list:
            content += self.render_content(VIEWS_MODEL_TEMPLATE, model)
        self.stdout.write(content)
        return content

    def get_forms_content(self):
        content = FORMS_HEADER.replace('<% ALL_MODELS %>', self.all_models_str)
        for model in self.model_list:
            content += self.render_content(FORMS_MODEL_TEMPLATE, model)
        self.stdout.write(content)
        return content

    def get_serializers_content(self):
        content = SERIALIZERS_HEADER.replace('<% ALL_MODELS %>', self.all_models_str)
        for model in self.model_list:
            content += self.render_content(SERIALIZERS_MODEL_TEMPLATE, model)
        self.stdout.write(content)
        return content

    def get_reverse_js(self):
        management.call_command('collectstatic_js_reverse')
        static_file = os.path.join(settings.BASE_DIR, 'static', 'django_js_reverse', 'js', 'reverse.js')
        self.make_folder(static_file)
        shutil.copyfile(os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js', 'reverse.js'), static_file)

    def run(self):
        self.stdout.write('\n######### %s #########' % self.urls_file)
        self.create_file(self.urls_file, self.get_urls_content())
        self.stdout.write('\n######### %s #########' % self.forms_file)
        self.create_file(self.forms_file, self.get_forms_content())
        self.stdout.write('\n######### %s #########' % self.views_file)
        self.create_file(self.views_file, self.get_views_content())
        self.stdout.write('\n######### %s #########' % self.serializers_file)
        self.create_file(self.serializers_file, self.get_serializers_content())

        for model in self.model_list:
            list_js_file = self.js_folder % model.__name__.lower()
            self.make_folder(list_js_file)
            self.stdout.write('\n######### %s #########' % list_js_file)
            content = self.render_content(LIST_JS, model)
            self.stdout.write(content)
            self.create_file(list_js_file, content)

            list_template_file = self.templates_folder % model.__name__.lower()
            self.make_folder(list_template_file)
            self.stdout.write('\n######### %s #########' % list_template_file)
            content = self.render_content(LIST_TEMPLATES, model)
            self.stdout.write(content)
            self.create_file(list_template_file, content)

        self.get_reverse_js()
        self.stdout.write('')
        self.stdout.write('')
        self.stderr.write('# Remember make below step:')
        self.stdout.write('')
        self.stderr.write(" * Add 'url(r'^', include('%s.urls')),' into super urls.py" % self.app_str)
        self.stdout.write('')
