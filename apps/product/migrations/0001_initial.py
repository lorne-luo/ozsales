# -*- coding: utf-8 -*-


from django.db import models, migrations
import apps.product.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('short_name', models.CharField(max_length=30, null=True, verbose_name='short_name', blank=True)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Country',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=128, verbose_name='name_en')),
                ('name_cn', models.CharField(max_length=128, null=True, verbose_name='name_cn', blank=True)),
                ('remarks', models.CharField(max_length=254, null=True, verbose_name='remarks', blank=True)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brand',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30, verbose_name='name')),
                ('remarks', models.CharField(max_length=254, null=True, verbose_name='remarks', blank=True)),
                ('parent_category', models.ForeignKey(default=None, blank=True, to='product.Category', null=True, verbose_name='parent cate')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(max_length=128, verbose_name='name_en')),
                ('name_cn', models.CharField(max_length=128, verbose_name='name_cn')),
                ('pic', models.ImageField(upload_to=apps.product.models.get_product_pic_path, null=True, verbose_name='picture', blank=True)),
                ('spec1', models.CharField(max_length=128, null=True, verbose_name='spec1', blank=True)),
                ('spec2', models.CharField(max_length=128, null=True, verbose_name='spec2', blank=True)),
                ('spec3', models.CharField(max_length=128, null=True, verbose_name='spec3', blank=True)),
                ('normal_price', models.DecimalField(null=True, verbose_name='normal price', max_digits=8, decimal_places=2, blank=True)),
                ('bargain_price', models.DecimalField(null=True, verbose_name='bargain price', max_digits=8, decimal_places=2, blank=True)),
                ('safe_sell_price', models.DecimalField(null=True, verbose_name='safe sell price', max_digits=8, decimal_places=2, blank=True)),
                ('brand', models.ForeignKey(verbose_name='brand', blank=True, to='product.Brand', null=True)),
                ('category', models.ManyToManyField(to='product.Category', null=True, verbose_name='category', blank=True)),
                ('page', models.ManyToManyField(to='store.Page', null=True, verbose_name='page', blank=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Product',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='brand',
            name='category',
            field=models.ManyToManyField(to='product.Category', null=True, verbose_name='category', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='brand',
            name='country',
            field=models.ForeignKey(verbose_name='country', blank=True, to='product.Country', null=True),
            preserve_default=True,
        ),
    ]
