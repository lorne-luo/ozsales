# -*- coding: utf-8 -*-


from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('messageset', '0004_auto_20160216_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(related_name=b'+', verbose_name='\u6536\u4ef6\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='notificationcontent',
            name='receivers',
            field=models.ManyToManyField(help_text='\u4e0d\u9009\u5219\u53d1\u9001\u7ed9\u5168\u4f53\u7528\u6237', related_name=b'notification_receivers', verbose_name='\u6536\u4ef6\u4eba', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='sitemailcontent',
            name='receivers',
            field=models.ManyToManyField(help_text='\u4e0d\u9009\u5219\u53d1\u9001\u7ed9\u5168\u4f53\u7528\u6237', related_name=b'sitemail_receivers', verbose_name='\u6536\u4ef6\u4eba', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
