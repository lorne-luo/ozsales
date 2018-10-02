from django.db import models
from django.db import connection
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from tenant_schemas.models import TenantMixin

from core.django.db import get_next_id

class TenantManager(models.Manager):
    def normal(self):
        qs = super(TenantManager, self).get_queryset().filter(schema_name__startswith=Tenant.SCHEMA_NAME_PREFIX)
        return qs

class Tenant(TenantMixin):
    """include domain_url and schema_name"""
    uuid = models.CharField(unique=True, max_length=12, null=True, blank=True)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True, null=True)

    auto_create_schema = True  # default true, schema will be automatically created and synced when it is saved
    DOMAIN_ROOT = 'youdan.com.au'

    SCHEMA_NAME_PREFIX = 't'
    objects = TenantManager()

    def __str__(self):
        return '%s' % self.schema_name

    def _generate_uuid(cls):
        # 3 alphabet and number
        return get_random_string(3, 'abcdefghijklmnopqrstuvwxyz1234567890')

    def set_uuid(self):
        if not self.uuid:
            _uuid = self._generate_uuid()
            while Tenant.objects.filter(uuid=_uuid).exists():
                _uuid = self._generate_uuid()
            self.uuid = _uuid

    def save(self, verbosity=1, *args, **kwargs):
        self.set_uuid()
        super(Tenant, self).save(verbosity, *args, **kwargs)

    @staticmethod
    def create_tenant():
        connection.set_schema_to_public()
        id = get_next_id(Tenant)
        tenant = Tenant(pk=id)

        schema_name = '%s%s' % (Tenant.SCHEMA_NAME_PREFIX, id)
        domain_url = '%s/%s' % (Tenant.DOMAIN_ROOT, id)
        tenant.schema_name = schema_name
        tenant.domain_url = domain_url
        tenant.save()
        tenant.create_schema(check_if_exists=True, verbosity=1)
        print('Tenant #%s created.' % tenant.pk)
        return tenant

    def set_schema(self):
        connection.set_schema(self.schema_name)

    @cached_property
    def seller(self):
        from apps.member.models import Seller
        old_schema=connection.schema_name
        self.set_schema()
        seller= Seller.objects.filter(tenant_id=str(self.id)).first()
        connection.set_schema(old_schema)
        return seller

    @cached_property
    def user(self):
        from core.auth_user.models import AuthUser
        return AuthUser.objects.filter(tenant_id=str(self.id)).first()
