# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20150715_2204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='total_product_price_aud',
            new_name='product_cost_aud',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='total_product_price_rmb',
            new_name='product_cost_rmb',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price_aud',
        ),
        migrations.RemoveField(
            model_name='order',
            name='total_price_rmb',
        ),
        migrations.AddField(
            model_name='order',
            name='sell_price',
            field=models.DecimalField(null=True, verbose_name='price RMB', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='total_cost_aud',
            field=models.DecimalField(null=True, verbose_name='Total Cost AUD', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='total_cost_rmb',
            field=models.DecimalField(null=True, verbose_name='Total Cost RMB', max_digits=8, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
