# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 06:40


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0008_expresscarrier_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expressorder',
            name='fee',
            field=models.DecimalField(decimal_places=2, default=0, help_text='\u8fd0\u8d39', max_digits=8, verbose_name='Shipping Fee'),
        ),
        migrations.AlterField(
            model_name='expressorder',
            name='track_id',
            field=models.CharField(help_text='\u8fd0\u5355\u53f7', max_length=30, verbose_name='Track ID'),
        ),
        migrations.AlterField(
            model_name='expressorder',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='\u91cd\u91cf', max_digits=8, null=True, verbose_name='Weight'),
        ),
    ]
