# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20160316_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid_time',
            field=models.DateTimeField(null=True, verbose_name='Paid Time', blank=True),
        ),
    ]
