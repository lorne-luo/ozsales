# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.DateField(verbose_name='Month')),
                ('cost_aud', models.DecimalField(default=0, verbose_name='Cost AUD', max_digits=8, decimal_places=2)),
                ('cost_rmb', models.DecimalField(null=True, verbose_name='Cost RMB', max_digits=8, decimal_places=2, blank=True)),
                ('shipping_fee', models.DecimalField(null=True, verbose_name='Shipping Fee', max_digits=8, decimal_places=2, blank=True)),
                ('sell_price_rmb', models.DecimalField(null=True, verbose_name='Sell Price RMB', max_digits=8, decimal_places=2, blank=True)),
                ('profit_rmb', models.DecimalField(null=True, verbose_name='Profit RMB', max_digits=8, decimal_places=2, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
