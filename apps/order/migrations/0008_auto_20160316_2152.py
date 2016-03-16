# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20160301_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paid_time',
            field=models.DateTimeField(verbose_name='Paid Time', null=True, editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'CREATED', max_length=20, verbose_name='status', choices=[(b'CREATED', '\u521b\u5efa'), (b'SHIPPING', '\u5728\u9014'), (b'DELIVERED', '\u5bc4\u8fbe'), (b'FINISHED', '\u5b8c\u6210')]),
        ),
    ]
