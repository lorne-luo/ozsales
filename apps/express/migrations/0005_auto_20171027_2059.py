# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    ExpressOrder = apps.get_model('express', 'ExpressOrder')
    ExpressOrder.objects.update(is_delivered=True)


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('express', '0004_auto_20160705_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='expressorder',
            name='is_delivered',
            field=models.BooleanField(default=False, verbose_name='is delivered'),
        ),
        migrations.AddField(
            model_name='expressorder',
            name='last_track',
            field=models.CharField(max_length=512, null=True, verbose_name='last track', blank=True),
        ),
        migrations.RunPython(forward, backward)
    ]
