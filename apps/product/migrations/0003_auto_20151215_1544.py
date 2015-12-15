# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20150924_1607'),
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
        migrations.AlterField(
            model_name='brand',
            name='country',
            field=models.ForeignKey(verbose_name='country', blank=True, to='product.Country', null=True),
        ),
    ]
