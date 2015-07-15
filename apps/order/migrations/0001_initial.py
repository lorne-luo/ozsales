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
                ('status', models.CharField(default=b'CREATED', max_length=20, verbose_name='status', choices=[(b'CREATED', b'CREATED'), (b'PURCHASED', b'PURCHASED'), (b'DELIVERED', b'DELIVERED'), (b'RECEIVED', b'RECEIVED'), (b'FINISHED', b'FINISHED')])),
                ('total_amount', models.IntegerField(default=0, verbose_name='amount')),
                ('total_product_price_aud', models.DecimalField(null=True, verbose_name='Product price AUD', max_digits=8, decimal_places=2, blank=True)),
                ('total_product_price_rmb', models.DecimalField(null=True, verbose_name='Product price RMB', max_digits=8, decimal_places=2, blank=True)),
                ('shipping_fee', models.DecimalField(null=True, verbose_name='shipping fee', max_digits=8, decimal_places=2, blank=True)),
                ('ship_time', models.DateTimeField(null=True, verbose_name='ship time', blank=True)),
                ('total_price_aud', models.DecimalField(null=True, verbose_name='Total AUD', max_digits=8, decimal_places=2, blank=True)),
                ('total_price_rmb', models.DecimalField(null=True, verbose_name='Total RMB', max_digits=8, decimal_places=2, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create time')),
                ('address', models.ForeignKey(verbose_name='address', blank=True, to='customer.Address', null=True)),
                ('customer', models.ForeignKey(verbose_name='customer', to='customer.Customer')),
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
                ('order', models.ForeignKey(verbose_name='Order', to='order.Order')),
                ('product', models.ForeignKey(verbose_name='Product', blank=True, to='product.Product', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
