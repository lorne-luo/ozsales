# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import core.auth_user.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='authuser',
            managers=[
                ('objects', core.auth_user.models.AuthUserManager()),
            ],
        ),
        migrations.AddField(
            model_name='authuser',
            name='mobile',
            field=models.CharField(max_length=30, verbose_name='mobile', blank=True),
        ),
    ]
