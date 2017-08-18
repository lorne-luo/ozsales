# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealSubscribe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('includes', models.CharField(max_length=255, verbose_name='includes')),
                ('excludes', models.CharField(max_length=255, null=True, verbose_name='excludes', blank=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, verbose_name='mobile', validators=[django.core.validators.RegexValidator(b'^[\\d-]+$', 'plz input validated mobile number', b'invalid')])),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('msg_count', models.IntegerField(null=True, verbose_name='message count', blank=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='create at', null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='OzbarginTask',
        ),
    ]
