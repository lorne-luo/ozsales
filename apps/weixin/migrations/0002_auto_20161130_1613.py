# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxapp',
            name='api_key',
            field=models.CharField(max_length=128, null=True, verbose_name='API Key', blank=True),
        ),
        migrations.AddField(
            model_name='wxapp',
            name='mch_id',
            field=models.CharField(max_length=128, null=True, verbose_name='MCH ID', blank=True),
        ),
    ]
