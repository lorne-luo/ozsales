# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_auto_20151230_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='groups',
            field=models.ManyToManyField(related_query_name='customer', related_name='customer_set', verbose_name='groups', to='auth.Group', blank=True),
        ),
    ]
