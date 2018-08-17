# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_auto_20170303_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.CharField(max_length=30, null=True, verbose_name='Coupon', blank=True),
        ),
    ]
