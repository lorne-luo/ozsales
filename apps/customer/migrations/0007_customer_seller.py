# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('customer', '0006_auto_20160203_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='seller',
            field=models.ForeignKey(verbose_name='Member', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
