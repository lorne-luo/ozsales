# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-01 04:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_auto_20171130_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='pinyin',
            field=models.TextField(blank=True, max_length=512, verbose_name='pinyin'),
        ),
        migrations.AddField(
            model_name='customer',
            name='pinyin',
            field=models.TextField(blank=True, max_length=512, verbose_name='pinyin'),
        ),
    ]