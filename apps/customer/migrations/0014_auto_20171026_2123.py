# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0013_auto_20170731_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='seller',
            field=models.ForeignKey(verbose_name='seller', blank=True, to='member.Seller', null=True),
        ),
    ]
