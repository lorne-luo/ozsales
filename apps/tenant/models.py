from django.db import models
from django.db import connection
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _
from tenant_schemas.models import TenantMixin

from core.django.db import get_postgres_next_id


class Tenant(TenantMixin):
    """include domain_url and schema_name"""
    # name = models.CharField(max_length=100)
    # paid_until = models.DateField()
    # on_trial = models.BooleanField(default=False)
    # created_on = models.DateField(auto_now_add=True)
    # seller = models.OneToOneField('member.Seller', on_delete=models.CASCADE, related_name='tenant', null=False, blank=False)
    uuid = models.CharField(unique=True, max_length=12, null=True, blank=True)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True, null=True)

    auto_create_schema = True  # default true, schema will be automatically created and synced when it is saved
    DOMAIN_ROOT = 'youdan.com.au'

    # class Meta():
    #     db_table = 'public.tenant_tenant'

    def _generate_uuid(cls):
        # 3 alphabet and 3 number
        alphabets = get_random_string(2, 'abcdefghijklmnopqrstuvwxyz1234567890')
        numbers = get_random_string(2, '1234567890')
        return alphabets + numbers

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
        id = get_postgres_next_id(Tenant)
        tenant = Tenant(id=id)

        schema_name = 't%s' % id
        domain_url = '%s/%s' % (Tenant.DOMAIN_ROOT, id)
        tenant.schema_name = schema_name
        tenant.domain_url = domain_url
        tenant.save()
        tenant.create_schema(check_if_exists=True, verbosity=1)
        print('Tenant #%s created.' % tenant.id)
        return tenant
