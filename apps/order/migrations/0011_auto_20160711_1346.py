# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_auto_20160704_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='amount',
            field=models.IntegerField(null=True, verbose_name='Amount', blank=True),
        ),
    ]
