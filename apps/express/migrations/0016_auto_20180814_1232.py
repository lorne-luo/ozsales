# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-14 02:32


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0015_expressorder_delivery_sms_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expressorder',
            name='delivery_sms_sent',
            field=models.BooleanField(default=False, verbose_name='delivery sms'),
        ),
    ]