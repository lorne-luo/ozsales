# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    MonthlyReport = apps.get_model('report', 'MonthlyReport')
    Seller = apps.get_model('member', 'Seller')
    luotao = Seller.objects.get(name='luotao')
    MonthlyReport.objects.update(seller=luotao)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('member', '0010_auto_20171106_1038'),
        ('report', '0002_auto_20160325_2345'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyreport',
            name='seller',
            field=models.ForeignKey(blank=True, to='member.Seller', null=True),
        ),
        migrations.RunPython(forward, backward)
    ]
