from __future__ import absolute_import, print_function, unicode_literals


def format_datetime(datetime, format_str='%Y-%m-%d %H:%M:%S'):
    return datetime.strftime(format_str)