# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_order_address_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='app_id',
            field=models.CharField(max_length=128, null=True, verbose_name='App ID', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=32, null=True, verbose_name='code', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_price',
            field=models.DecimalField(null=True, verbose_name='Payment Price', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='remark',
            field=models.CharField(max_length=512, null=True, verbose_name='remark', blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'CREATED', max_length=20, verbose_name='status', choices=[(b'CREATED', '\u521b\u5efa'), (b'CONFIRMED', '\u786e\u8ba4'), (b'SHIPPING', '\u5728\u9014'), (b'DELIVERED', '\u5bc4\u8fbe'), (b'FINISHED', '\u5b8c\u6210'), (b'CANCELED', '\u53d6\u6d88'), (b'CLOSED', '\u5173\u95ed')]),
        ),
    ]
