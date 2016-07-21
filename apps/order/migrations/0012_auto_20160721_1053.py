# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20160711_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='origin_sell_rmb',
            field=models.DecimalField(null=True, verbose_name='Origin RMB', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_cost_aud',
            field=models.DecimalField(null=True, verbose_name='Cost AUD', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_fee',
            field=models.DecimalField(null=True, verbose_name='Ship Fee', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_cost_aud',
            field=models.DecimalField(null=True, verbose_name='Total AUD', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_cost_rmb',
            field=models.DecimalField(null=True, verbose_name='Total RMB', max_digits=8, decimal_places=2, blank=True),
        ),
    ]
