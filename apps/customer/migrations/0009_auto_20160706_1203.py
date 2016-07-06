# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_auto_20160704_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(to='customer.InterestTag', verbose_name='Tags', blank=True),
        ),
    ]
