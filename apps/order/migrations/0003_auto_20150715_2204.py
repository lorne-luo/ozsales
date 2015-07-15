# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20150715_2156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='profit_aud',
        ),
        migrations.AlterField(
            model_name='order',
            name='profit_rmb',
            field=models.DecimalField(null=True, verbose_name='profit RMB', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(related_name=b'products', verbose_name='Order', to='order.Order'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(verbose_name='Product', blank=True, to='product.Product', null=True),
        ),
    ]
