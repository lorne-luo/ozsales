# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0013_auto_20170118_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='app_id',
            field=models.CharField(default=None, max_length=128, verbose_name='App ID'),
            preserve_default=False,
        ),
    ]
