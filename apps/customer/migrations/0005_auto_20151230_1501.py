# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0004_auto_20151215_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email', blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_order_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Last order time', null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile', validators=[django.core.validators.RegexValidator(b'^[\\d-]+$', 'plz input validated mobile number', b'invalid')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='primary_address',
            field=models.ForeignKey(related_name='primary address', verbose_name='Primary Address', blank=True, to='customer.Address', null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='remarks',
            field=models.CharField(max_length=128, null=True, verbose_name='Remarks', blank=True),
        ),
    ]
