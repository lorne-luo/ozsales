from django.db import models
from django.utils.translation import ugettext_lazy as _
from tenant_schemas.models import TenantMixin


class Tenant(TenantMixin):
    """include domain_url and schema_name"""
    # name = models.CharField(max_length=100)
    # paid_until = models.DateField()
    # on_trial = models.BooleanField(default=False)
    # created_on = models.DateField(auto_now_add=True)
    seller = models.OneToOneField('member.Seller', on_delete=models.CASCADE, related_name='tenant', null=False, blank=False)
    enable = models.BooleanField(default=True)
    create_at = models.DateTimeField(_('create at'), auto_now_add=True, null=True)

    auto_create_schema = True  # default true, schema will be automatically created and synced when it is saved
