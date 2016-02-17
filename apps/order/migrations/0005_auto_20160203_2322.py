# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20160109_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='finish_time',
            field=models.DateTimeField(verbose_name='Finish Time'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ship_time',
            field=models.DateTimeField(null=True, verbose_name='Shipping Time', blank=True),
        ),
    ]
