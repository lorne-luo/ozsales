# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0004_auto_20170121_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wxpayment',
            name='cash_fee',
        ),
        migrations.RemoveField(
            model_name='wxpayment',
            name='cash_fee_type',
        ),
        migrations.RemoveField(
            model_name='wxpayment',
            name='coupon_count',
        ),
        migrations.RemoveField(
            model_name='wxpayment',
            name='coupon_fee',
        ),
        migrations.AddField(
            model_name='wxpayment',
            name='sign_type',
            field=models.CharField(default=b'MD5', max_length=32, null=True, blank=True),
        ),
    ]
