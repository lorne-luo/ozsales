# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-06 06:36
from __future__ import unicode_literals

import core.django.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarrierTracker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_cn', models.CharField(help_text='中文名称', max_length=255, verbose_name='中文名称')),
                ('name_en', models.CharField(blank=True, help_text='英文名称', max_length=255, verbose_name='英文名称')),
                ('pinyin', models.TextField(blank=True, max_length=512, verbose_name='pinyin')),
                ('domain', models.CharField(blank=True, help_text='domain', max_length=512, verbose_name='domain')),
                ('website', models.URLField(blank=True, help_text='官方网站地址', verbose_name='官网地址')),
                ('search_url', models.URLField(blank=True, help_text='查询网页地址', verbose_name='查询网址')),
                ('post_search_url', models.URLField(blank=True, help_text='查询提交网址', verbose_name='查询提交网址')),
                ('id_upload_url', models.URLField(blank=True, help_text='证件上传地址', verbose_name='证件上传地址')),
                ('rate', models.DecimalField(blank=True, decimal_places=2, help_text='每公斤费率', max_digits=6, null=True, verbose_name='费率')),
                ('is_default', models.BooleanField(default=False, help_text='是否默认', verbose_name='默认')),
                ('track_id_regex', models.CharField(blank=True, help_text='订单号正则表达式', max_length=512, verbose_name='单号正则')),
            ],
            bases=(core.django.models.PinYinFieldModelMixin, models.Model),
        ),
    ]