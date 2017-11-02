# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        ('product', '0005_auto_20160721_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='full_price',
            field=models.DecimalField(null=True, verbose_name='full price', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sell_price',
            field=models.DecimalField(null=True, verbose_name='sell price', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
    ]
