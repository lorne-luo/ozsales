# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('store', '0001_initial'),
        ('order', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(verbose_name='Product', blank=True, to='product.Product', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='store',
            field=models.ForeignKey(verbose_name='Store', blank=True, to='store.Store', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(verbose_name='address', blank=True, to='customer.Address', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(verbose_name='customer', to='customer.Customer'),
            preserve_default=True,
        ),
    ]
