# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('member', '0009_auto_20171025_0913'),
        ('order', '0018_orderproduct_is_purchased'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(verbose_name='seller', blank=True, to='member.Seller', null=True),
        ),
        migrations.RenameField(
            model_name='order',
            old_name='code',
            new_name='order_id'
        ),
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=32, null=True, verbose_name='order id', blank=True),
        ),
    ]
