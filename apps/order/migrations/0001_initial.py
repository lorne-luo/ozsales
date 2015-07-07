# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_amount', models.IntegerField(default=0, verbose_name='amount')),
                ('total_product_price_aud', models.DecimalField(null=True, verbose_name='Product price AUD', max_digits=8, decimal_places=2, blank=True)),
                ('total_product_price_rmb', models.DecimalField(null=True, verbose_name='Product price RMB', max_digits=8, decimal_places=2, blank=True)),
                ('shipping_fee', models.DecimalField(null=True, verbose_name='shipping fee', max_digits=8, decimal_places=2, blank=True)),
                ('total_price_aud', models.DecimalField(null=True, verbose_name='Total AUD', max_digits=8, decimal_places=2, blank=True)),
                ('total_price_rmb', models.DecimalField(null=True, verbose_name='Total RMB', max_digits=8, decimal_places=2, blank=True)),
                ('customer', models.ForeignKey(verbose_name='Customer', to='customer.Customer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price_aud', models.DecimalField(null=True, verbose_name='price AUD', max_digits=8, decimal_places=2, blank=True)),
                ('price_rmb', models.DecimalField(null=True, verbose_name='price RMB', max_digits=8, decimal_places=2, blank=True)),
                ('amount', models.IntegerField(default=0, verbose_name='amount')),
                ('total_price_aud', models.DecimalField(null=True, verbose_name='Total AUD', max_digits=8, decimal_places=2, blank=True)),
                ('total_price_rmb', models.DecimalField(null=True, verbose_name='Total RMB', max_digits=8, decimal_places=2, blank=True)),
                ('product', models.ForeignKey(verbose_name='Product', to='product.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='order.OrderProduct', verbose_name='Product'),
            preserve_default=True,
        ),
    ]
