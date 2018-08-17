# -*- coding: utf-8 -*-

import uuid
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Product = apps.get_model("product", "product")
    for p in Product.objects.all():
        if not p.uuid:
            uuid_str = uuid.uuid4().hex
            while (Product.objects.filter(uuid=uuid_str).exists()):
                uuid_str = uuid.uuid4().hex

            p.uuid = uuid_str
            p.save()
        print(p.id, p.uuid)


def backwarad_func(apps, schema_editor):
    print("nothing to migrate")


class Migration(migrations.Migration):
    dependencies = [
        ('product', '0006_auto_20170115_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='uuid',
            field=models.CharField(max_length=36, unique=True, null=True, blank=True),
        ),
        migrations.RunPython(forwards_func, backwarad_func),

    ]
