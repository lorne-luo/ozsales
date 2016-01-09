# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20150922_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'CREATED', max_length=20, verbose_name='status', choices=[(b'CREATED', b'CREATED'), (b'SHIPPING', b'SHIPPING'), (b'DELIVERED', b'DELIVERED'), (b'FINISHED', b'FINISHED')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.IntegerField(default=0, verbose_name='Amount'),
        ),
    ]
