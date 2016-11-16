# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20160706_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='short_name',
            field=models.CharField(max_length=128, null=True, verbose_name='Abbr', blank=True),
        ),
    ]
