# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forward(apps, schema_editor):
    OrderProduct = apps.get_model('order', 'OrderProduct')
    OrderProduct.objects.all().exclude(order__status='CREATED').exclude(order__status='CONFIRMED').update(is_purchased=True)


def backward(apps, schema_editor):
    # do nothing
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0017_order_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='is_purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(forward, backward)
    ]
