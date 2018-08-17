# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 03:24


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0017_auto_20180203_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='city',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='country',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='groupid',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='headimg_url',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='is_subscribe',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='language',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='nickname',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='openid',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='privilege',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='province',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='subscribe_time',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='unionid',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='weixin_id',
        ),
        migrations.AddField(
            model_name='customer',
            name='auth_user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL),
        ),
    ]
