# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_seller_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email address', blank=True),
        ),
    ]
