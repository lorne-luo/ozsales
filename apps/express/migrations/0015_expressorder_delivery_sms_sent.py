# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-13 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0014_auto_20180430_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='expressorder',
            name='delivery_sms_sent',
            field=models.BooleanField(default=False, verbose_name='delivery msg'),
        ),
    ]
