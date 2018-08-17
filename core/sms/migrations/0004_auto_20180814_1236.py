# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-14 02:36


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_auto_20180812_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sms',
            name='request_id',
        ),
        migrations.RemoveField(
            model_name='sms',
            name='url',
        ),
        migrations.AddField(
            model_name='sms',
            name='biz_id',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='biz_id'),
        ),
        migrations.AddField(
            model_name='sms',
            name='template_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='template code'),
        ),
    ]
