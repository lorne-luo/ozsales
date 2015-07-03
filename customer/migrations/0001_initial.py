# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('email', models.EmailField(max_length=254, unique=True, null=True, verbose_name='email address', blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined', null=True)),
            ],
            options={
                'verbose_name': 'customer',
                'verbose_name_plural': 'customers',
                'permissions': (),
            },
            bases=(models.Model,),
        ),
    ]
