# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0005_auto_20171027_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='expresscarrier',
            name='track_id_regex',
            field=models.CharField(max_length=512, verbose_name='number regex', blank=True),
        ),
    ]
