# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tb_url',
            field=models.URLField(null=True, verbose_name='TB URL', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='wd_url',
            field=models.URLField(null=True, verbose_name='WD URL', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='wx_url',
            field=models.URLField(null=True, verbose_name='WX URL', blank=True),
            preserve_default=True,
        ),
    ]
