# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='mobile',
            field=models.CharField(max_length=18, null=True, blank=True),
            preserve_default=True,
        ),
    ]
