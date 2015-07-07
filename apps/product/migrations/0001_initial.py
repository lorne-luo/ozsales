# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brand',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('remarks', models.CharField(max_length=500, null=True, verbose_name='remarks', blank=True)),
                ('parent_category', models.ForeignKey(default=None, blank=True, to='product.Category', null=True, verbose_name='Parent_Cate')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Category',
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_cn', models.CharField(max_length=254, verbose_name='name')),
                ('name_en', models.CharField(max_length=254, null=True, verbose_name='name', blank=True)),
                ('brand', models.ForeignKey(verbose_name='Brand', blank=True, to='product.Brand', null=True)),
                ('category', models.ForeignKey(verbose_name='Category', blank=True, to='product.Category', null=True)),
                ('page', models.ManyToManyField(to='store.Page', null=True, verbose_name='Page', blank=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Product',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='brand',
            name='category',
            field=models.ForeignKey(verbose_name='Category', blank=True, to='product.Category', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='brand',
            name='country',
            field=models.ForeignKey(verbose_name='Country', blank=True, to='product.Country', null=True),
            preserve_default=True,
        ),
    ]
