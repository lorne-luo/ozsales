# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0004_auto_20160705_1158'),
        ('customer', '0014_auto_20171026_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='expressorder',
            name='latest_track',
            field=models.CharField(max_length=512, null=True, verbose_name='latest track', blank=True),
        ),
    ]
