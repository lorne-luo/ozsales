# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'CREATED', max_length=20, verbose_name='status', choices=[(b'CREATED', b'CREATED'), (b'PAID', b'PAID'), (b'SHIPPING', b'SHIPPING'), (b'DELIVERED', b'DELIVERED'), (b'FINISHED', b'FINISHED')])),
                ('total_amount', models.IntegerField(default=0, verbose_name='Total Amount')),
                ('product_cost_aud', models.DecimalField(null=True, verbose_name='Product Cost AUD', max_digits=8, decimal_places=2, blank=True)),
                ('product_cost_rmb', models.DecimalField(null=True, verbose_name='Product Cost RMB', max_digits=8, decimal_places=2, blank=True)),
                ('shipping_fee', models.DecimalField(null=True, verbose_name='Shipping Fee', max_digits=8, decimal_places=2, blank=True)),
                ('ship_time', models.DateTimeField(verbose_name='Shipping Time', null=True, editable=False, blank=True)),
                ('total_cost_aud', models.DecimalField(null=True, verbose_name='Total Cost AUD', max_digits=8, decimal_places=2, blank=True)),
                ('total_cost_rmb', models.DecimalField(null=True, verbose_name='Total Cost RMB', max_digits=8, decimal_places=2, blank=True)),
                ('origin_sell_rmb', models.DecimalField(null=True, verbose_name='Origin Sell RMB', max_digits=8, decimal_places=2, blank=True)),
                ('sell_price_rmb', models.DecimalField(null=True, verbose_name='Sell Price RMB', max_digits=8, decimal_places=2, blank=True)),
                ('profit_rmb', models.DecimalField(null=True, verbose_name='Profit RMB', max_digits=8, decimal_places=2, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('finish_time', models.DateTimeField(auto_now_add=True, verbose_name='Finish Time')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, null=True, verbose_name='Name', blank=True)),
                ('amount', models.IntegerField(default=0, verbose_name='Amount')),
                ('sell_price_rmb', models.DecimalField(null=True, verbose_name='Sell Price RMB', max_digits=8, decimal_places=2, blank=True)),
                ('total_price_rmb', models.DecimalField(null=True, verbose_name='Total RMB', max_digits=8, decimal_places=2, blank=True)),
                ('cost_price_aud', models.DecimalField(null=True, verbose_name='Cost Price AUD', max_digits=8, decimal_places=2, blank=True)),
                ('total_price_aud', models.DecimalField(null=True, verbose_name='Total AUD', max_digits=8, decimal_places=2, blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('order', models.ForeignKey(related_name=b'products', verbose_name='Order', to='order.Order')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
