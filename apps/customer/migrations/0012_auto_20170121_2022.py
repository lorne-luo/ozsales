# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20170117_1223'),
        ('customer', '0011_auto_20170110_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(null=True, verbose_name='Amount', blank=True)),
                ('product', models.ForeignKey(verbose_name='Product', blank=True, to='product.Product', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='cart',
            field=models.ManyToManyField(to='customer.CartProduct', verbose_name='cart', blank=True),
        ),
    ]
