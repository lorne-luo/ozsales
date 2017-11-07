# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0010_auto_20171106_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='email',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='mobile',
        ),
        migrations.AlterField(
            model_name='seller',
            name='auth_user',
            field=models.OneToOneField(related_name='seller', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='seller',
            name='name',
            field=models.CharField(max_length=30, null=True, verbose_name='name', blank=True),
        ),
    ]
