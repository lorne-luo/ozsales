# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20160203_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='finish_time',
            field=models.DateTimeField(null=True, verbose_name='Finish Time', blank=True),
        ),
    ]
