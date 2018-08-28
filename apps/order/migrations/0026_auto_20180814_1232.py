# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-14 02:32


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0025_auto_20180810_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('CREATED', '\u521b\u5efa'), ('SHIPPING', '\u5728\u9014'), ('DELIVERED', '\u5bc4\u8fbe'), ('FINISHED', '\u5b8c\u6210'), ('CLOSED', '\u5173\u95ed')], default='CREATED', max_length=20, verbose_name='\u72b6\u6001'),
        ),
    ]