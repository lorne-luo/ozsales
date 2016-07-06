# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20150924_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='category',
            field=models.ManyToManyField(to='product.Category', verbose_name='category', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(to='product.Category', verbose_name='category', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='page',
            field=models.ManyToManyField(to='store.Page', verbose_name='page', blank=True),
        ),
    ]
