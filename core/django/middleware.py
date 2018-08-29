from django.contrib.auth.middleware import AuthenticationMiddleware
from tenant_schemas.middleware import DefaultTenantMiddleware
from tenant_schemas.utils import get_public_schema_name


class ProfileAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        super(ProfileAuthenticationMiddleware, self).process_request(request)
        profile = getattr(request.user, 'profile', None)
        setattr(request, 'profile', profile)
        if profile:
            if request.user.is_seller:
                setattr(request, 'seller', profile)
            if request.user.is_customer:
                setattr(request, 'customer', profile)


class MyTenantMiddleware(DefaultTenantMiddleware):
    DEFAULT_SCHEMA_NAME = 'public'

    def get_tenant(self, model, hostname, request):
        # todo entry for login, register etc.
        try:
            return super(DefaultTenantMiddleware, self).get_tenant(
                model, hostname, request)
        except model.DoesNotExist:
            schema_name = self.DEFAULT_SCHEMA_NAME
            if not schema_name:
                schema_name = get_public_schema_name()

            return model.objects.get(schema_name=schema_name)
