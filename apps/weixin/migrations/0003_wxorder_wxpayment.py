# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weixin', '0002_auto_20161130_1613'),
    ]

    operations = [
        migrations.CreateModel(
            name='WxOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('return_code', models.CharField(blank=True, max_length=16, null=True, choices=[(b'FAIL', b'FAIL'), (b'SUCCESS', b'SUCCESS')])),
                ('return_msg', models.CharField(max_length=128, null=True, blank=True)),
                ('result_code', models.CharField(blank=True, max_length=16, null=True, choices=[(b'FAIL', b'FAIL'), (b'SUCCESS', b'SUCCESS')])),
                ('appid', models.CharField(max_length=32, null=True, blank=True)),
                ('mch_id', models.CharField(max_length=32, null=True, blank=True)),
                ('device_info', models.CharField(max_length=32, null=True, blank=True)),
                ('nonce_str', models.CharField(max_length=32, null=True, blank=True)),
                ('sign', models.CharField(max_length=32, null=True, blank=True)),
                ('err_code', models.CharField(max_length=32, null=True, blank=True)),
                ('err_code_des', models.CharField(max_length=128, null=True, blank=True)),
                ('trade_type', models.CharField(max_length=16, null=True, blank=True)),
                ('prepay_id', models.CharField(max_length=64, null=True, blank=True)),
                ('code_url', models.CharField(max_length=32, null=True, blank=True)),
                ('xml_response', models.TextField(null=True, blank=True)),
                ('order', models.OneToOneField(to='order.Order')),
            ],
        ),
        migrations.CreateModel(
            name='WxPayment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('transaction_id', models.CharField(max_length=32, null=True, blank=True)),
                ('return_code', models.CharField(blank=True, max_length=16, null=True, choices=[(b'FAIL', b'FAIL'), (b'SUCCESS', b'SUCCESS')])),
                ('return_msg', models.CharField(max_length=128, null=True, blank=True)),
                ('result_code', models.CharField(blank=True, max_length=16, null=True, choices=[(b'FAIL', b'FAIL'), (b'SUCCESS', b'SUCCESS')])),
                ('appid', models.CharField(max_length=32, null=True, blank=True)),
                ('mch_id', models.CharField(max_length=32, null=True, blank=True)),
                ('device_info', models.CharField(max_length=32, null=True, blank=True)),
                ('nonce_str', models.CharField(max_length=32, null=True, blank=True)),
                ('sign', models.CharField(max_length=32, null=True, blank=True)),
                ('err_code', models.CharField(max_length=32, null=True, blank=True)),
                ('err_code_des', models.CharField(max_length=128, null=True, blank=True)),
                ('openid', models.CharField(max_length=128, null=True, blank=True)),
                ('is_subscribe', models.BooleanField(default=False)),
                ('trade_type', models.CharField(max_length=16, null=True, blank=True)),
                ('bank_type', models.CharField(max_length=16, null=True, blank=True)),
                ('total_fee', models.PositiveIntegerField(null=True, blank=True)),
                ('fee_type', models.CharField(max_length=8, null=True, blank=True)),
                ('cash_fee', models.PositiveIntegerField(null=True, blank=True)),
                ('cash_fee_type', models.CharField(max_length=16, null=True, blank=True)),
                ('coupon_fee', models.PositiveIntegerField(null=True, blank=True)),
                ('coupon_count', models.PositiveIntegerField(null=True, blank=True)),
                ('out_trade_no', models.CharField(max_length=32, null=True, blank=True)),
                ('attach', models.CharField(max_length=128, null=True, blank=True)),
                ('time_end', models.CharField(max_length=16, null=True, blank=True)),
                ('trade_state', models.CharField(blank=True, max_length=32, null=True, choices=[(b'SUCCESS', b'\xe6\x94\xaf\xe4\xbb\x98\xe6\x88\x90\xe5\x8a\x9f'), (b'REFUND', b'\xe5\xb7\xb2\xe9\x80\x80\xe6\xac\xbe'), (b'NOTPAY', b'\xe6\x9c\xaa\xe4\xbb\x98\xe6\xac\xbe'), (b'CLOSED', b'\xe6\x94\xaf\xe4\xbb\x98\xe5\x85\xb3\xe9\x97\xad'), (b'REVOKED', b'\xe5\xb7\xb2\xe6\x92\xa4\xe9\x94\x80'), (b'USERPAYING', b'\xe6\x94\xaf\xe4\xbb\x98\xe4\xb8\xad'), (b'PAYERROR', b'\xe6\x94\xaf\xe4\xbb\x98\xe5\xa4\xb1\xe8\xb4\xa5')])),
                ('trade_state_desc', models.CharField(max_length=256, null=True, blank=True)),
                ('xml_response', models.TextField(null=True, blank=True)),
                ('order', models.OneToOneField(to='order.Order')),
            ],
        ),
    ]
