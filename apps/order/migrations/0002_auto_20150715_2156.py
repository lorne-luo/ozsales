# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='profit_aud',
            field=models.DecimalField(null=True, verbose_name='profit', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='profit_rmb',
            field=models.DecimalField(null=True, verbose_name='profit', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'CREATED', max_length=20, verbose_name='status', choices=[(b'CREATED', b'CREATED'), (b'PAID', b'PAID'), (b'DELIVERED', b'DELIVERED'), (b'RECEIVED', b'RECEIVED'), (b'FINISHED', b'FINISHED')]),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(related_name=b'products', verbose_name='Product', blank=True, to='product.Product', null=True),
        ),
    ]
