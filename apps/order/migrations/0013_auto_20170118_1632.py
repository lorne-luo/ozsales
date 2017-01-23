# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def copy_address(apps, schema_editor):
    Order = apps.get_model("order", "Order")

    for o in Order.objects.all():
        if o.address:
            o.address_copy = '%s,%s,%s' % (o.address.name, o.address.mobile, o.address.address)
            o.save(update_fields=['address_copy'])


def backwarad_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_auto_20160721_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address_copy',
            field=models.CharField(max_length=512, null=True, verbose_name='address', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='code',
            field=models.CharField(max_length=32, null=True, verbose_name='code', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_price',
            field=models.DecimalField(null=True, verbose_name='Payment Price', max_digits=8, decimal_places=2, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='remark',
            field=models.CharField(max_length=512, null=True, verbose_name='remark', blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default=b'CREATED', max_length=20, verbose_name='status', choices=[(b'CREATED', '\u521b\u5efa'), (b'SHIPPING', '\u5728\u9014'), (b'DELIVERED', '\u5bc4\u8fbe'), (b'FINISHED', '\u5b8c\u6210'), (b'CANCELED', '\u53d6\u6d88')]),
        ),
        migrations.AddField(
            model_name='order',
            name='app_id',
            field=models.CharField(default=None, max_length=128, verbose_name='App ID'),
            preserve_default=False,
        ),
        migrations.RunPython(copy_address, backwarad_func),
    ]
