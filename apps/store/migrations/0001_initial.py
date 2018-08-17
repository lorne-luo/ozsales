# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=254, verbose_name='name')),
                ('url', models.URLField(verbose_name='url')),
                ('price', models.DecimalField(verbose_name='price', max_digits=8, decimal_places=2)),
                ('original_price', models.DecimalField(verbose_name='original price', max_digits=8, decimal_places=2)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Page',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('short_name', models.CharField(max_length=30, null=True, verbose_name='short name', blank=True)),
                ('address', models.CharField(max_length=128, null=True, verbose_name='address', blank=True)),
                ('domain', models.URLField(null=True, verbose_name='domain', blank=True)),
                ('search_url', models.URLField(null=True, verbose_name='Search URL', blank=True)),
                ('shipping_rate', models.CharField(max_length=30, null=True, verbose_name='Shipping Rate', blank=True)),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Store',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='page',
            name='store',
            field=models.ForeignKey(verbose_name='Store', blank=True, to='store.Store', null=True),
            preserve_default=True,
        ),
    ]
