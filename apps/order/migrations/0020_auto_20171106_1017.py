# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0019_auto_20171026_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(blank=True, to='member.Seller', null=True),
        ),
    ]
