# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('member', '0008_auto_20171025_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='auth_user',
            field=models.OneToOneField(related_name='seller', null=True, blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='seller',
            name='expire_at',
            field=models.DateField(null=True, verbose_name='member expire at', blank=True),
        ),
        migrations.AddField(
            model_name='seller',
            name='start_at',
            field=models.DateField(null=True, verbose_name='member start at', blank=True),
        ),
    ]
