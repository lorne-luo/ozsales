from django.db import connection
from tenant_schemas.middleware import DefaultTenantMiddleware
from tenant_schemas.utils import get_public_schema_name


class ProfileTenantMiddleware(DefaultTenantMiddleware):
    """
    Selects the proper database schema using the request host. E.g. <my_tenant>.<my_domain>
    """
    DEFAULT_SCHEMA_NAME = get_public_schema_name()

    def get_tenant(self, model, hostname, request):
        tenant = None
        if request.user.is_authenticated() and request.user.tenant_id:
            tenant = model.objects.filter(pk=request.user.tenant_id).first()

        schema_name = self.DEFAULT_SCHEMA_NAME or get_public_schema_name()
        return tenant or model.objects.get(schema_name=schema_name)

    def process_request(self, request):
        super(ProfileTenantMiddleware, self).process_request(request)

        if request.user.is_authenticated():
            profile = getattr(request.user, 'profile', None)
            setattr(request, 'profile', profile)
            if profile:
                if request.user.is_seller:
                    setattr(request, 'seller', profile)
                if request.user.is_customer:
                    setattr(request, 'customer', profile)
