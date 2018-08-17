# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0012_auto_20170303_1217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customercart',
            old_name='final_price',
            new_name='payment_price',
        ),
    ]
