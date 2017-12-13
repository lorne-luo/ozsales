# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 22:16
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Product = apps.get_model("product", "product")
    for p in Product.objects.all():
        if p.brand:
            p.brand_cn = p.brand.name_cn
            p.brand_en = p.brand.name_en
            p.save()


def backwarad_func(apps, schema_editor):
    print "nothing to migrate"


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0012_customproduct_defaultproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='country',
        ),
        migrations.AddField(
            model_name='product',
            name='brand_cn',
            field=models.CharField(blank=True, max_length=128, verbose_name='brand_cn'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand_en',
            field=models.CharField(blank=True, max_length=128, verbose_name='brand_en'),
        ),
        migrations.AddField(
            model_name='product',
            name='country',
            field=models.CharField(blank=True,
                                   choices=[(b'AU', '\u6fb3\u6d32'), (b'US', '\u5317\u7f8e'), (b'EU', '\u6fb3\u6d32'),
                                            (b'GB', '\u82f1\u56fd'), (b'JP', '\u65e5\u672c'), (b'KR', '\u97e9\u56fd'),
                                            (b'TW', '\u53f0\u6e7e'), (b'SEA', '\u4e1c\u5357\u4e9a')], default=b'AU',
                                   max_length=128, verbose_name='country'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name_cn',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='name_cn'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brand',
            name='remarks',
            field=models.CharField(blank=True, default='', max_length=254, verbose_name='remarks'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='brand',
            name='short_name',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Abbr'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='code'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='name_cn',
            field=models.CharField(blank=True, max_length=128, verbose_name='name_cn'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_en',
            field=models.CharField(blank=True, max_length=128, verbose_name='name_en'),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.RunPython(forwards_func, backwarad_func),
    ]