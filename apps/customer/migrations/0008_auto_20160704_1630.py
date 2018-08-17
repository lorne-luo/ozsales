# -*- coding: utf-8 -*-


from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0007_customer_seller'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customer',
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='primary_address',
            field=models.ForeignKey(related_name='primary_address', verbose_name='Primary Address', blank=True, to='customer.Address', null=True),
        ),
    ]
