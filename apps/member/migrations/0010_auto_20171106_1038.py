# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_auto_20171025_0913'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_at', models.DateField(null=True, verbose_name='membership start at', blank=True)),
                ('end_at', models.DateField(null=True, verbose_name='membership expire at', blank=True)),
                ('amount', models.DecimalField(null=True, verbose_name='membership payment', max_digits=5, decimal_places=2)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='create at', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='seller',
            name='mobile',
            field=models.CharField(default='', max_length=18, blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='membershiporder',
            name='seller',
            field=models.ForeignKey(blank=True, to='member.Seller', null=True),
        ),
    ]
