# -*- coding: utf-8 -*-


from django.db import migrations, models


def forward(apps, schema_editor):
    Order = apps.get_model('order', 'Order')
    for o in Order.objects.all():
        if o.total_cost_aud:
            o.aud_rmb_rate = o.total_cost_rmb / o.total_cost_aud
            o.save()


def backward(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0013_order_aud_rmb_rate'),
    ]

    operations = [
        migrations.RunPython(forward, backward)
    ]
