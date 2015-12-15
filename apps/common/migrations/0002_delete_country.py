# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20151215_1544'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Country',
        ),
    ]
