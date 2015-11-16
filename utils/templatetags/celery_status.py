import logging
from django import template
from celery.task.control import inspect
from socket import error as socket_error


log = logging.getLogger(__name__)
register = template.Library()

def get_celery_data():
    try:
        stats = inspect().stats() # Takes roughly 1s!
    except socket_error:
        log.warn('Socket error when trying to check celery status.')
        return {}

    if not stats:
        return {}

    server = stats.itervalues().next() # go to first (and only) entry in the dict

    server_data = {'name': server}
    server_data['broker_hostname'] = server['broker']['hostname']
    server_data['broker_port'] = server['broker']['port']
    server_data['broker_userid'] = server['broker']['userid']
    server_data['broker_transport'] = server['broker']['transport']
    server_data['tasks'] = ((key, server['total'].get(key)) for key in server['total'])

    return server_data


class CeleryStatus(template.Node):
    def render(self, context):
        context['celery_connection'] = {'state': False}

        data = get_celery_data()
        if data:
            context['celery_stats'] = data
            context['celery_connection'] = {'state': True}
        return ''


@register.tag
def get_celery_stats(parser, token):
    return CeleryStatus()
