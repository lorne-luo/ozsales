import os
import shutil
from django.core import management
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = ''' Update js_reverse

    Usage: python manage.py js_reverse

    '''

    def handle(self, *args, **options):
        management.call_command('collectstatic_js_reverse')
        static_file = os.path.join(settings.BASE_DIR, 'static', 'django_js_reverse', 'js', 'reverse.js')
        collectstatic_file = os.path.join(settings.STATIC_ROOT, 'django_js_reverse', 'js', 'reverse.js')

        self.make_folder(static_file)
        shutil.copyfile(collectstatic_file, static_file)

        self.stdout.write(
            'js-reverse.js written to %s' % os.path.join('static', 'django_js_reverse', 'js', 'reverse.js'))

    def make_folder(self, path):
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)