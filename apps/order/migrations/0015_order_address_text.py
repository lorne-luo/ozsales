# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    Order = apps.get_model('order', 'Order')
    for o in Order.objects.all():
        if o.address:
            o.address_text = u'%s,%s,%s' % (o.address.name, o.address.mobile, o.address.address)
            o.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0014_update_aud_rmb_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address_text',
            field=models.CharField(max_length=255, null=True, verbose_name='address_text', blank=True),
        ),
        migrations.RunPython(forward, backward)
    ]
