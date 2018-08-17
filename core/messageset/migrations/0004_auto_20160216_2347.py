# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messageset', '0003_auto_20160209_2215'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='receive',
            new_name='receiver',
        ),
        migrations.RenameField(
            model_name='sitemailreceive',
            old_name='receive',
            new_name='receiver',
        ),
    ]
