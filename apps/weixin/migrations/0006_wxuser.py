# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 03:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('weixin', '0005_auto_20170123_2340'),
    ]

    operations = [
        migrations.CreateModel(
            name='WxUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weixin_id', models.CharField(blank=True, max_length=32)),
                ('is_subscribe', models.BooleanField(default=False)),
                ('nickname', models.CharField(blank=True, max_length=32)),
                ('openid', models.CharField(blank=True, max_length=64)),
                ('sex', models.CharField(blank=True, max_length=5)),
                ('province', models.CharField(blank=True, max_length=32)),
                ('city', models.CharField(blank=True, max_length=32)),
                ('country', models.CharField(blank=True, max_length=32)),
                ('language', models.CharField(blank=True, max_length=64)),
                ('headimg_url', models.URLField(blank=True, max_length=256)),
                ('privilege', models.CharField(blank=True, max_length=256)),
                ('unionid', models.CharField(blank=True, max_length=64)),
                ('subscribe_time', models.DateField(blank=True, null=True)),
                ('groupid', models.CharField(blank=True, max_length=256)),
                ('auth_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wxuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]