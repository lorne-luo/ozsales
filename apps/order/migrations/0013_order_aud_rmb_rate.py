# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('order', '0012_auto_20160721_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='aud_rmb_rate',
            field=models.DecimalField(null=True, verbose_name='AUD-RMB', max_digits=8, decimal_places=4, blank=True),
        ),
    ]
