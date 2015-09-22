# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import apps.customer.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, verbose_name='mobile number', validators=[django.core.validators.RegexValidator(b'^[\\d-]+$', 'plz input validated mobile number', b'invalid')])),
                ('address', models.CharField(max_length=50, verbose_name='address')),
                ('id_number', models.CharField(max_length=20, null=True, verbose_name='ID number', blank=True)),
                ('id_photo_front', models.ImageField(upload_to=apps.customer.models.get_id_photo_front_path, null=True, verbose_name='ID Front', blank=True)),
                ('id_photo_back', models.ImageField(upload_to=apps.customer.models.get_id_photo_back_path, null=True, verbose_name='ID Back', blank=True)),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Address',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='email address', blank=True)),
                ('mobile', models.CharField(blank=True, max_length=15, null=True, verbose_name='mobile number', validators=[django.core.validators.RegexValidator(b'^[\\d-]+$', 'plz input validated mobile number', b'invalid')])),
                ('remarks', models.CharField(max_length=128, null=True, verbose_name='remarks', blank=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined', null=True)),
                ('groups', models.ManyToManyField(related_query_name=b'customer', related_name=b'customer_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A customer will get all permissions granted to each of his/her group.', verbose_name='customer groups')),
                ('primary_address', models.ForeignKey(related_name='primary address', verbose_name='primary address', blank=True, to='customer.Address', null=True)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customer',
                'permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InterestTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30, verbose_name='name')),
                ('remarks', models.CharField(max_length=254, null=True, verbose_name='remarks', blank=True)),
            ],
            options={
                'verbose_name': 'InterestTag',
                'verbose_name_plural': 'InterestTags',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='customer',
            name='tags',
            field=models.ManyToManyField(to='customer.InterestTag', null=True, verbose_name='Tags', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='customer',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name=b'customer', related_name=b'customer_set', to='auth.Permission', blank=True, help_text='Specific permissions for this customer.', verbose_name='customer permissions'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='address',
            name='customer',
            field=models.ForeignKey(verbose_name='customer', to='customer.Customer'),
            preserve_default=True,
        ),
    ]
