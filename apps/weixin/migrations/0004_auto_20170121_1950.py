# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0003_wxorder_wxpayment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wxapp',
            name='api_key',
        ),
        migrations.RemoveField(
            model_name='wxorder',
            name='code_url',
        ),
        migrations.AddField(
            model_name='wxapp',
            name='mch_key',
            field=models.CharField(max_length=128, null=True, verbose_name='MCH Key', blank=True),
        ),
        migrations.AddField(
            model_name='wxorder',
            name='total_fee',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
