# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_auto_20161115_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, blank=True)),
                ('nickname', models.CharField(max_length=32, null=True, blank=True)),
                ('wx_openid', models.CharField(max_length=64, null=True, blank=True)),
                ('wx_id', models.CharField(max_length=32, null=True, blank=True)),
                ('headimg_url', models.CharField(max_length=256, null=True, blank=True)),
                ('mobile', models.CharField(max_length=18, null=True, blank=True)),
                ('sex', models.CharField(max_length=5, null=True, blank=True)),
                ('country', models.CharField(max_length=32, null=True, blank=True)),
                ('province', models.CharField(max_length=32, null=True, blank=True)),
                ('city', models.CharField(max_length=32, null=True, blank=True)),
                ('subscribe_time', models.DateField(null=True, blank=True)),
                ('unionid', models.CharField(max_length=64, null=True, blank=True)),
                ('remark', models.CharField(max_length=256, null=True, blank=True)),
                ('group_id', models.IntegerField(null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
