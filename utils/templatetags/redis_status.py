from django import template
from django.conf import settings
import redis

register = template.Library()

DETAILED_STATS = ('redis_version',
                  'connected_clients',
                  'used_cpu_sys',
                  'used_cpu_user',
                  'used_memory_human',
                  'used_memory_peak_human',
                  'max_memory_human',
                  'mem_fragmentation_ratio',
                  'keyspace_hits',
                  'keyspace_misses',
                  'expired_keys',
                  'evicted_keys',)

def _prettyname (name):
    return ' '.join([word.capitalize() for word in name.split('_')])

def _human_bytes (bytes):
    bytes = float(bytes)
    if bytes >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif bytes >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fB' % bytes
    return size


class RedisStatus(template.Node):
    def render (self, context):
        server_stats = []
        try:
            client = redis.Redis(port=settings.REDIS_PORT, host=settings.REDIS_HOST)
            server_data = {'url' : '%s/%s' % (settings.BROKER_URL, settings.REDIS_DB)}
            server_data['max_memory'] = client.config_get()['maxmemory']
            stats = client.info()
            stats['max_memory_human'] = _human_bytes(server_data['max_memory'])
            server_data['used_memory'] = stats['used_memory']
            server_data['keyspace_misses'] = stats['keyspace_misses']
            server_data['key_operations'] = stats['keyspace_hits'] + stats['keyspace_misses']
            server_data['detailed_stats'] = ((_prettyname(key), stats.get(key, 'Not supported'),) for key in DETAILED_STATS)
            server_stats.append(server_data)
            context['redis_connection'] = {'state': True}
            context['server_stats'] = server_stats
        except redis.ConnectionError:
            context['redis_connection'] = {'state': False}
        return ''

@register.tag
def get_redis_stats (parser, token):
    return RedisStatus()
