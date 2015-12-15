# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20151117_1558'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='seller',
            options={'verbose_name': 'seller', 'verbose_name_plural': 'sellers'},
        ),
    ]
