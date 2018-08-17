# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_product_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=32, null=True, verbose_name='code', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(null=True, verbose_name='description', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='sold_count',
            field=models.IntegerField(default=0, verbose_name='Sold Count'),
        ),
        migrations.AddField(
            model_name='product',
            name='state',
            field=models.CharField(default=b'ON_SELL', choices=[(b'ON_SELL', b'ON_SELL'), (b'NOT_SELL', b'NOT_SELL'), (b'NO_STOCK', b'NO_STOCK')], max_length=32, blank=True, null=True, verbose_name='state'),
        ),
        migrations.AddField(
            model_name='product',
            name='summary',
            field=models.TextField(null=True, verbose_name='summary', blank=True),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(null=True, verbose_name='weight', max_digits=8, decimal_places=2, blank=True),
        ),
    ]
