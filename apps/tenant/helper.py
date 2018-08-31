from django.db import connection



def get_tenants_map():
    return {
        "thor.polls.local": "thor",
        "potter.polls.local": "potter",
    }

def hostname_from_request(request):
    # split on `:` to remove port
    return request.get_host().split(':')[0].lower()


def tenant_schema_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname)


def set_tenant_schema_for_request(request):
    schema = tenant_schema_from_request(request)
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path to {schema}")


class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_tenant_schema_for_request(request)
        response = self.get_response(request)
        return response

# MIDDLEWARE = [
#     'tenants.middlewares.TenantMiddleware',
# ]

def set_search_path(sender, **kwargs):
    from django.conf import settings

    conn = kwargs.get('connection')
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SET search_path={}".format(
            settings.SEARCH_PATH,
        ))
