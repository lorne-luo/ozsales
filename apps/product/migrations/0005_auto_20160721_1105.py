# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_brand_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name_en',
            field=models.CharField(unique=True, max_length=128, verbose_name='name_en'),
        ),
    ]
