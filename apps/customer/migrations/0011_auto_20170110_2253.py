# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20170110_2251'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='country',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='groupid',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='headimg_url',
            field=models.URLField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='is_subscribe',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='language',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='nickname',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='openid',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='privilege',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='province',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='remark',
            field=models.CharField(max_length=128, null=True, verbose_name='Remark', blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='sex',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='subscribe_time',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='unionid',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='customer',
            name='weixin_id',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='seller',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='Member'),
        ),
    ]
