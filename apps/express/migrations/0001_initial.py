# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpressCarrier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_cn', models.CharField(max_length=50, verbose_name='name_cn')),
                ('name_en', models.CharField(max_length=50, null=True, verbose_name='name_en', blank=True)),
                ('website', models.URLField(null=True, verbose_name='website', blank=True)),
                ('search_url', models.URLField(null=True, verbose_name='search url', blank=True)),
                ('rate', models.DecimalField(null=True, verbose_name='rate', max_digits=6, decimal_places=2, blank=True)),
            ],
            options={
                'verbose_name': 'Express Carrier',
                'verbose_name_plural': 'Express Carrier',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ExpressOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('track_id', models.CharField(max_length=30, verbose_name='Track ID')),
                ('fee', models.DecimalField(null=True, verbose_name='Shipping Fee', max_digits=8, decimal_places=2, blank=True)),
                ('weight', models.DecimalField(null=True, verbose_name='Weight', max_digits=8, decimal_places=2, blank=True)),
                ('id_upload', models.BooleanField(default=False, verbose_name='ID uploaded')),
                ('remarks', models.CharField(max_length=128, null=True, verbose_name='remarks', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Create Time')),
                ('address', models.ForeignKey(verbose_name='address', blank=True, to='customer.Address', null=True)),
                ('carrier', models.ForeignKey(verbose_name='carrier', to='express.ExpressCarrier')),
            ],
            options={
                'verbose_name': 'Express Order',
                'verbose_name_plural': 'Express Order',
            },
            bases=(models.Model,),
        ),
    ]
