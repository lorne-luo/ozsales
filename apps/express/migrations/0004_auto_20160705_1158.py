# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('express', '0003_auto_20160704_1630'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='expressorder',
            unique_together=set([('carrier', 'track_id')]),
        ),
    ]
