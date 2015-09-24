# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_order_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='last order time', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='order_count',
            field=models.PositiveIntegerField(default=0, null=True, verbose_name='Order Count', blank=True),
            preserve_default=True,
        ),
    ]
