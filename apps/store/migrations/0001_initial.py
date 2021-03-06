# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-10 23:43
from __future__ import unicode_literals

import core.django.db
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=254, verbose_name='name')),
                ('url', models.URLField(verbose_name='url')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='price')),
                ('original_price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='original price')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Page',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.IntegerField()),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('schema_name', models.CharField(blank=True, default=core.django.db.get_schema_name, max_length=32)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('short_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='short name')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='address')),
                ('domain', models.URLField(blank=True, null=True, verbose_name='domain')),
                ('search_url', models.URLField(blank=True, null=True, verbose_name='Search URL')),
                ('shipping_rate', models.CharField(blank=True, max_length=30, null=True, verbose_name='Shipping Rate')),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Store',
            },
        ),
        migrations.AddField(
            model_name='page',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Store', verbose_name='Store'),
        ),
    ]
