# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0001_initial'),
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expressorder',
            name='order',
            field=models.ForeignKey(related_name=b'express_orders', verbose_name='order', to='order.Order'),
            preserve_default=True,
        ),
    ]
