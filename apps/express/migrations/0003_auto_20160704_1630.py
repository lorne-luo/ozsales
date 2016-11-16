# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0002_expressorder_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='expresscarrier',
            name='is_default',
            field=models.BooleanField(default=False, verbose_name=b'Default'),
        ),
        migrations.AlterField(
            model_name='expresscarrier',
            name='rate',
            field=models.DecimalField(null=True, verbose_name='Rate', max_digits=6, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='expresscarrier',
            name='search_url',
            field=models.URLField(null=True, verbose_name='Search url', blank=True),
        ),
        migrations.AlterField(
            model_name='expresscarrier',
            name='website',
            field=models.URLField(null=True, verbose_name='Website', blank=True),
        ),
        migrations.AlterField(
            model_name='expressorder',
            name='carrier',
            field=models.ForeignKey(verbose_name='carrier', blank=True, to='express.ExpressCarrier', null=True),
        ),
        migrations.AlterField(
            model_name='expressorder',
            name='remarks',
            field=models.CharField(max_length=128, null=True, verbose_name='Remarks', blank=True),
        ),
    ]
