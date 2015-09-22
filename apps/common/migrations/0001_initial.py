# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('short_name', models.CharField(max_length=30, null=True, verbose_name='short_name', blank=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Country',
            },
            bases=(models.Model,),
        ),
    ]
