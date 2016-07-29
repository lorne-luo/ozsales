# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20160320_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='sell_price_rmb',
            field=models.DecimalField(null=True, verbose_name='Final RMB', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_time',
            field=models.DateTimeField(null=True, verbose_name='Ship Time', blank=True),
        ),
    ]
