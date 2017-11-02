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
            ],
            options={
                'verbose_name': 'CartProduct',
                'verbose_name_plural': 'CartProducts',
            },
        ),
        migrations.CreateModel(
            name='CustomerCart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coupon', models.CharField(max_length=30, null=True, verbose_name='Coupon', blank=True)),
                ('origin_price', models.DecimalField(null=True, verbose_name='Origin Price', max_digits=8, decimal_places=2, blank=True)),
                ('final_price', models.DecimalField(null=True, verbose_name='Price', max_digits=8, decimal_places=2, blank=True)),
                ('customer', models.OneToOneField(verbose_name='Customer', to='customer.Customer')),
            ],
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='cart',
            field=models.ForeignKey(related_name='products', verbose_name='Cart', blank=True, to='customer.CustomerCart', null=True),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(verbose_name='Product', blank=True, to='product.Product', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='cartproduct',
            unique_together=set([('cart', 'product')]),
        ),
    ]
