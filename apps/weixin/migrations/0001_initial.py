# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-09-04 11:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WxApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('app_id', models.CharField(max_length=128, verbose_name='App ID')),
                ('app_secret', models.CharField(max_length=128, verbose_name='App Secret')),
                ('mch_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='MCH ID')),
                ('mch_key', models.CharField(blank=True, max_length=128, null=True, verbose_name='MCH Key')),
                ('access_token', models.CharField(blank=True, max_length=512, null=True, verbose_name='Access Token')),
                ('token_expiry', models.DateTimeField(blank=True, null=True, verbose_name='Token Expiry')),
                ('jsapi_ticket', models.CharField(blank=True, max_length=512, null=True, verbose_name='JsApi Ticket')),
                ('ticket_expiry', models.DateTimeField(blank=True, null=True, verbose_name='Ticket Expiry')),
                ('update_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Update At')),
            ],
            options={
                'verbose_name': 'Weixin App',
                'verbose_name_plural': 'Weixin Apps',
            },
        ),
        migrations.CreateModel(
            name='WxOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_code', models.CharField(blank=True, choices=[('FAIL', 'FAIL'), ('SUCCESS', 'SUCCESS')], max_length=16, null=True)),
                ('return_msg', models.CharField(blank=True, max_length=128, null=True)),
                ('result_code', models.CharField(blank=True, choices=[('FAIL', 'FAIL'), ('SUCCESS', 'SUCCESS')], max_length=16, null=True)),
                ('appid', models.CharField(blank=True, max_length=32, null=True)),
                ('mch_id', models.CharField(blank=True, max_length=32, null=True)),
                ('device_info', models.CharField(blank=True, max_length=32, null=True)),
                ('nonce_str', models.CharField(blank=True, max_length=32, null=True)),
                ('sign', models.CharField(blank=True, max_length=32, null=True)),
                ('err_code', models.CharField(blank=True, max_length=32, null=True)),
                ('err_code_des', models.CharField(blank=True, max_length=128, null=True)),
                ('trade_type', models.CharField(blank=True, max_length=16, null=True)),
                ('prepay_id', models.CharField(blank=True, max_length=64, null=True)),
                ('total_fee', models.PositiveIntegerField(blank=True, null=True)),
                ('xml_response', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WxPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(blank=True, max_length=32, null=True)),
                ('return_code', models.CharField(blank=True, choices=[('FAIL', 'FAIL'), ('SUCCESS', 'SUCCESS')], max_length=16, null=True)),
                ('return_msg', models.CharField(blank=True, max_length=128, null=True)),
                ('result_code', models.CharField(blank=True, choices=[('FAIL', 'FAIL'), ('SUCCESS', 'SUCCESS')], max_length=16, null=True)),
                ('appid', models.CharField(blank=True, max_length=32, null=True)),
                ('mch_id', models.CharField(blank=True, max_length=32, null=True)),
                ('device_info', models.CharField(blank=True, max_length=32, null=True)),
                ('nonce_str', models.CharField(blank=True, max_length=32, null=True)),
                ('sign', models.CharField(blank=True, max_length=32, null=True)),
                ('sign_type', models.CharField(blank=True, default='MD5', max_length=32, null=True)),
                ('err_code', models.CharField(blank=True, max_length=32, null=True)),
                ('err_code_des', models.CharField(blank=True, max_length=128, null=True)),
                ('openid', models.CharField(blank=True, max_length=128, null=True)),
                ('is_subscribe', models.BooleanField(default=False)),
                ('trade_type', models.CharField(blank=True, max_length=16, null=True)),
                ('bank_type', models.CharField(blank=True, max_length=16, null=True)),
                ('total_fee', models.PositiveIntegerField(blank=True, null=True)),
                ('fee_type', models.CharField(blank=True, max_length=8, null=True)),
                ('out_trade_no', models.CharField(blank=True, max_length=32, null=True)),
                ('attach', models.CharField(blank=True, max_length=128, null=True)),
                ('time_end', models.CharField(blank=True, max_length=16, null=True)),
                ('trade_state', models.CharField(blank=True, choices=[('SUCCESS', '支付成功'), ('REFUND', '已退款'), ('NOTPAY', '未付款'), ('CLOSED', '支付关闭'), ('REVOKED', '已撤销'), ('USERPAYING', '支付中'), ('PAYERROR', '支付失败')], max_length=32, null=True)),
                ('trade_state_desc', models.CharField(blank=True, max_length=256, null=True)),
                ('xml_response', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WxUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weixin_id', models.CharField(blank=True, max_length=32)),
                ('is_subscribe', models.BooleanField(default=False)),
                ('nickname', models.CharField(blank=True, max_length=32)),
                ('openid', models.CharField(blank=True, max_length=64)),
                ('sex', models.CharField(blank=True, max_length=5)),
                ('province', models.CharField(blank=True, max_length=32)),
                ('city', models.CharField(blank=True, max_length=32)),
                ('country', models.CharField(blank=True, max_length=32)),
                ('language', models.CharField(blank=True, max_length=64)),
                ('headimg_url', models.URLField(blank=True, max_length=256)),
                ('privilege', models.CharField(blank=True, max_length=256)),
                ('unionid', models.CharField(blank=True, max_length=64)),
                ('subscribe_time', models.DateField(blank=True, null=True)),
                ('groupid', models.CharField(blank=True, max_length=256)),
                ('auth_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wxuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
