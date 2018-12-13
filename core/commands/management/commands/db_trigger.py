import os
import re
from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Q
from django.db.models import FileField
from django.db import connection
from django.conf import settings


# in this function content splits and checks line by line
def _runsql(f):
    with connection.cursor() as c:
        file_data = f.readlines()
        statement = ''
        delimiter = ';\n'
        for line in file_data:
            if re.findall('DELIMITER', line):  # found delimiter
                if re.findall('^\s*DELIMITER\s+(\S+)\s*$', line):
                    delimiter = re.findall('^\s*DELIMITER\s+(\S+)\s*$', line)[0] + '\n'
                    continue
                else:
                    raise SyntaxError('Your usage of DELIMITER is not correct, go and fix it!')
            # add lines while not met lines with current delimiter
            statement += line
            if line.endswith(delimiter):
                if delimiter != ';\n':
                    # found delimiter, add dash symbols (or any symbols you want) for converting MySQL statements with multiply delimiters in SQL statement
                    statement = statement.replace(';', '; --').replace(delimiter, ';')
                print(statement + '\n')
                # execute current statement
                c.execute(statement)
                # begin collect next statement
                statement = ''


def run_sql_file(path):
    """this function get sql file"""
    filepath = os.path.join(settings.BASE_DIR, path)
    with open(filepath, 'rt') as f:
        return _runsql(f)


class Command(BaseCommand):
    help = "This command deletes all media files from the MEDIA_ROOT directory which are no longer referenced by any of the models from installed_apps"

    def handle(self, *args, **options):
        run_sql_file('postgres.sql')
        print('Postgres DB trigger and function created.')
